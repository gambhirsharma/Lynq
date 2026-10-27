# Fleet ops: running the constellation as a KubeEdge cluster

NTN-Pulse treats every satellite as a regenerative gNB with onboard compute. With 30 satellites (and ~6 replacements
a year), the software on them becomes a fleet problem: rolling out a new gNB build, a policy-engine update or an edge
analytics app to every satellite safely, and knowing which version runs where. This note looks at handling that with
**KubeEdge** (a CNCF project that extends Kubernetes to edge nodes with intermittent links) and backs the trade-offs
with numbers from `ntnpulse/fleet.py` (dashboard tab **Fleet ops**).

## Architecture

```
Frankfurt cloud                       Gateways (7)            Satellites (12 -> 30)
+--------------------------+         +-----------+          +-------------------------------+
| Kubernetes control plane |  fibre  | feeder    |  X/Ka    | EdgeCore (edge agent)          |
| + KubeEdge CloudCore     |-------->| uplink    |--------->|  - gNB container (CU/DU)       |
| + image registry (OCI)   |         +-----------+          |  - NTN-Pulse policy agent      |
| + NTN-Pulse twin/policy  |                        RF/opt  |  - local state DB (autonomy)   |
+--------------------------+                        ISL <-> |  - cached image layers         |
                                                            +-------------------------------+
```

- **One edge node per satellite.** Labels carry plane, slot, payload type (OQ or hosted), and optical terminal yes/no.
- **Desired state lives in the cloud.** A satellite picks it up at its next contact, direct or over the ISL mesh,
  then runs on it autonomously. EdgeCore keeps pods and their config in a local database and keeps them running
  while disconnected.
- **Rollout = canary + waves.** Pre-pull the image everywhere first (KubeEdge `ImagePrePullJob`), release one canary,
  soak it, then release waves of `maxUnavailable` satellites, interleaved across planes so no ISL ring loses
  several nodes at once. Restarts are gated to when the satellite is **not over the service area**.
- **Ground fallback.** If the onboard gNB is down, the payload drops back to bent-pipe through a ground gNB, as in
  the proposal's risk table.

## What the twin shows (24 h, 100 MB image delta, 5 Mbps feeder share, 90 s gNB restart)

| Fleet | Control path | Reachable | Longest silence | NotReady / sat / day* | Fleet updated in |
|---|---|---:|---:|---:|---:|
| 12 (today, SSO) | direct only | 10% | 287 min | 14 | 8.6 h |
| 12 (today, SSO) | + ISL | 12% | 287 min | 17 | 7.1 h |
| 30 (SSO) | direct only | 10% | 287 min | 14 | **21 h** |
| 30 (SSO) | + ISL | ~100% | <1 min | 0 | **1.2 h** |
| 30 (65° delta) | + ISL | 100% | 0 min | 0 | 1.4 h |

\* With the stock 40 s `node-monitor-grace-period`. Nearly every one of those gaps also runs past the default 300 s
`unreachable` toleration, so an untuned cluster would **evict pods ~14 times per satellite per day** on today's fleet.

Other results:
- **Waves stay inside the limit.** At most 3 satellites were down at once, with 0 s of North Sea outage when restarts
  are gated to outside the basin. "All at once" finishes in 0.4 h but took 17 of 30 satellites down together.
- **Peer sharing** (satellites passing layers to ISL neighbours) moved 10–25% of the bytes off the feeder links.
  It matters most when the image is large or the feeder share is small.
- **The ISL also carries the control plane.** It does more than shorten alarm latency. Without it, each wave has to
  wait for its satellites to come round to a gateway and report back, so 30 satellites take *longer* to update than 12.

## Pros

1. **One declarative model for the whole fleet.** Every satellite's software, version and config is in Git
   (GitOps: Argo CD/Flux → Kubernetes → KubeEdge). "Which build runs on sat 17?" becomes a query.
2. **Safe, staged rollouts out of the box.** Canary, waves, `maxUnavailable`, health probes and rollback come from
   Kubernetes. With 30 satellites and ~6 swaps a year, that matters more than it does at 12.
3. **Built for bad links.** KubeEdge is designed for nodes that disconnect. EdgeCore keeps workloads running from local
   state, syncs over a single multiplexed websocket/QUIC tunnel, and only sends deltas. Vanilla Kubernetes is not.
4. **Same tooling on the ground and in orbit.** The ground 5G Core, the NTN-Pulse twin and the onboard apps share one
   API, one CI/CD pipeline, one monitoring stack and one security model (mTLS, RBAC, signed images).
5. **Hosted payloads and multi-tenancy.** Namespaces and node labels make it natural to run third-party apps on spare
   onboard compute: one route to the "hosted payload" revenue in the proposal.
6. **Mature and open.** CNCF graduated, Apache-2.0, no vendor lock-in. Gives OQ a story for European sovereignty
   that a proprietary vendor stack does not.

## Cons

1. **Kubernetes assumes connectivity, orbit does not.** Untuned, today's 12 satellites would flap NotReady
   ~14 times a day each and have their pods evicted. It needs careful tuning: long or infinite `unreachable`
   tolerations, longer grace periods, and alerts based on predicted contact windows instead of heartbeats.
2. **Onboard footprint.** EdgeCore + a container runtime need roughly 70–150 MB RAM and some CPU. That is fine on a
   Linux-class payload computer, but radiation-tolerant flight computers are small and may not run Linux containers
   at all. The gNB's real-time PHY/L1 usually runs on FPGA/DSP, so only the upper layers (CU/DU-high, apps) fit
   in containers.
3. **Bandwidth for images.** Container layers are big compared with a 5–20 Mbps feeder share. Without layer deltas,
   pre-staging and compression, an update competes with paying traffic (the slider in the dashboard shows the cost).
4. **Flight software qualification.** Space agencies and insurers expect frozen, qualified binaries. A dynamic
   orchestrator is harder to certify than a fixed image with A/B partitions. Most likely only *non-flight-critical*
   payload software goes through KubeEdge, while the bus/AOCS stays on the classic TT&C path.
5. **Security surface.** A cluster-wide control plane that can push code to every satellite is a high-value target.
   It needs signed images, hardware root of trust onboard, a separate command authentication layer, and possibly
   export-control (ITAR/EAR) review for crypto.
6. **Not built for space.** KubeEdge does not know about orbits, contact windows or ISL routing. The orbit awareness
   (when to release, when to restart, which path) has to come from NTN-Pulse. That is extra work, but it is also
   where Lynq adds value.

## Alternatives

| Option | Fits when | Trade-off |
|---|---|---|
| **KubeEdge** | Linux-class payload computer, many apps, ground already runs Kubernetes | Best disconnected-edge support in the Kubernetes family; needs orbit-aware tuning |
| **k3s / MicroK8s per satellite** | Each satellite is managed alone | A full control plane per satellite: heavy, and no single fleet view without extra tooling |
| **OpenYurt / SuperEdge** | Similar to KubeEdge | Similar features, smaller community, weaker offline autonomy story |
| **Eclipse ioFog / balena / Mender** | Containers or A/B images without Kubernetes | Simpler and lighter, with delta OTA built in, but no Kubernetes API or ecosystem |
| **Custom TT&C + A/B partitions** | Flight-critical software | Easiest to qualify, slowest to iterate |
| **Space-native app platforms** (e.g. "app store in orbit" offerings) | Hosted payloads on someone else's bus | Ready-made, but lock-in, and the satellites are not yours |

**Recommendation for the proposal:** keep KubeEdge on the *payload compute* (gNB upper layers, NTN-Pulse policy agent,
hosted apps) and leave the bus/flight software on the classic TT&C path. Tune it for orbit, and let NTN-Pulse drive
the rollouts (release, restart windows, peer distribution), since it already knows the contact plan.

## Model limits

- Reachability uses the same ISL geometry as the traffic twin: links are assumed acquired whenever they are in range.
  Optical acquisition time would add silence at 30 satellites.
- Image transfer uses a fixed feeder share and a fixed RF ISL share. It does not compete with user traffic
  in the same run.
- Health checks always pass. A failed canary (rollback) is not modelled.
- Heartbeats are evaluated against the stock Kubernetes timers only, to show why tuning is needed.

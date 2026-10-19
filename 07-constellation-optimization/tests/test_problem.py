"""Genome encoding, repair and stage-0 pruning."""
import numpy as np

import problem as pb
from globalnet import config as cfg

STAR = (87.0, "star")


def test_genome_roundtrip():
    g = pb.genome([dict(alt=550, family=STAR, planes=12, spp=20)], 2)
    d = pb.design(pb.repair(g, 2, 800), 2)
    assert len(d.shells) == 1 and d.shells[0].label == "12x20@550km/87deg/star" and d.size == 240


def test_repair_is_canonical_and_idempotent():
    rng = np.random.default_rng(0)
    sizes = pb.gene_sizes(2)
    for _ in range(200):
        g = pb.repair(tuple(int(rng.integers(s)) for s in sizes), 2, 800)
        assert pb.repair(g, 2, 800) == g
        assert pb.design(g, 2).size <= 800


def test_repair_drops_rf_inplane_that_cannot_close():
    g = pb.repair(pb.genome([dict(alt=800, family=STAR, planes=6, spp=11, tech_in="rf")], 1), 1, 800)
    assert pb.design(g, 1).shells[0].isl.tech_in == "none"


def test_inactive_shell_and_inter_shell_are_canonical():
    one = pb.genome([dict(alt=550, family=STAR, planes=12, spp=20)], 2, inter_shell=True)
    assert pb.repair(one, 2, 800)[-1] == 0          # inter-shell links need two shells


def test_tiny_design_is_pruned_without_simulating():
    g = pb.repair(pb.genome([dict(alt=550, family=STAR, planes=2, spp=2)], 1), 1, 800)
    r = pb.evaluate_genome(g, pb.Settings(max_shells=1))
    assert not r["simulated"] and r["violation"] > 0


def test_evaluate_genome_returns_objectives():
    g = pb.repair(pb.genome([dict(alt=1200, family=STAR, planes=8, spp=15)], 1), 1, 800)
    r = pb.evaluate_genome(g, pb.Settings(max_shells=1, hours=1, step_s=120, grid=400))
    assert r["simulated"] and r["violation"] == 0 and r["f_cost"] > 0 and 60 < r["f_latency"] < 150

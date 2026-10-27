# Lynq NTN-Pulse website

A one-page static site for the project, built with plain HTML, CSS and JS. There is no build step and nothing to install.

## Run locally

```bash
cd website
python -m http.server 8000   # then open http://localhost:8000
```

## Deploy on Vercel

1. Import the repo in Vercel.
2. Set **Root Directory** to `website`.
3. Set Framework Preset to **Other**, and leave the build and output settings empty.

Or deploy from the CLI: `cd website && npx vercel --prod`.

## Contact

The contact address is set in `CONTACT_EMAIL` at the top of `script.js`. The contact form opens the visitor's email app, so no backend is needed.

## Files

| Path | What it is |
|---|---|
| `index.html` | Single page: hero, problem, solution, proposal (tabs), team, contact. Content matches the final pitch |
| `styles.css` | Site styles, built on the brand tokens |
| `script.js` | Mobile menu, proposal tabs, mailto contact form |
| `assets/lynq-tokens.css` | Copy of `02-brand/lynq-brand-kit/tokens/lynq-tokens.css` |
| `assets/logos/`, `assets/favicon/` | Copies from the brand kit (orbital-link mark, dark variant) |
| `assets/docs/` | Copies of the final pitch (`08-final-pitch/Lynq-NTN-Pulse-final-pitch.pdf`) and the Phase 1 proposal (`03-proposal/current/final.pdf`, `.docx`) |

If the deck or proposal changes, copy the new files into `assets/docs/` again.

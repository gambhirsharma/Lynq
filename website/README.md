# Lynq NTN-Pulse website

A one-page static site for the proposal, built with plain HTML, CSS and JS. There is no build step and nothing to install.

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

## Before going live

- Set the real contact address in `CONTACT_EMAIL` at the top of `script.js`. The contact form opens the visitor's email app, so no backend is needed.

## Files

| Path | What it is |
|---|---|
| `index.html` | Single page: hero, problem, solution, proposal (tabs), team, contact |
| `styles.css` | Site styles, built on the brand tokens |
| `script.js` | Mobile menu, proposal tabs, mailto contact form |
| `assets/lynq-tokens.css` | Copy of `02-brand/lynq-brand-kit/tokens/lynq-tokens.css` |
| `assets/logos/`, `assets/favicon/` | Copies from the brand kit (orbital-link mark, dark variant) |
| `assets/docs/` | Copies of `03-proposal/current/final.pdf` and `.docx` |

If the proposal changes, copy the new PDF and DOCX into `assets/docs/` again.

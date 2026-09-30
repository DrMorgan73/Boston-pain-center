# Boston Pain Center — Website

Commercial static website for Boston Pain Center (Boston, MA). Built with a Python
generator (`build.py`) that produces plain HTML/CSS/vanilla-JS — no build step needed
to edit output, but **edit `build.py` and re-run `python3 build.py`** rather than
hand-editing generated HTML, so header/footer/nav stay consistent.

## Structure

- `*.html` — 22 pages (generated; see `build.py` `main()`)
- `guides/` — 3 printable preparation guides (generated)
- `assets/css/style.css` — design system
- `assets/js/main.js` — nav, EN/ES toggle, accordions, filters, forms, booking flow
- `assets/js/payment-config.js` — **Stripe Payment Links go here** (empty until BPC provides them)
- `content/pricing.json` — service prices (empty = "price to be confirmed")
- `content/video-tips.json` — daily video tips (Dr. Roberto Feliz)
- `content/podcast.json` — weekly podcast episodes (Dr. Roberto Feliz)

## Owner to-dos before launch

1. **Prices** — fill `price` in `content/pricing.json` (leave `""` until confirmed).
2. **Stripe links** — paste BPC Stripe Payment Links into `assets/js/payment-config.js`.
   Empty links show "Online payment activating soon — call to book" (never a dead button).
3. **Contact details** — phone/address/hours are placeholders marked "to be verified".
4. **Physician bios & portraits** — both doctors show monogram placeholders; bios publish after verification.
5. **Pictures** — owner to supply; swap into page templates when ready.
6. **Content** — add daily tips to `content/video-tips.json`, weekly episodes to `content/podcast.json`
   (field format documented in each file's `_instructions`).
7. **HIPAA backend** — all forms are browser-side demos with reference numbers. Connect a
   HIPAA-compliant form/scheduling backend before collecting real patient information.

## Rebuild

```bash
python3 build.py
```

## Deploy

Any static host (Vercel, Netlify, GitHub Pages). `404.html` included.

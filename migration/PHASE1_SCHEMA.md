# Phase 1 — content schema (metaalhandel-gids.nl)

**Approved** with Phase 0 (same shape as other niches). Collection: `metaalhandels`.

One JSON file per listing: `src/content/metaalhandels/{provincie}--{plaats}--{slug}.json`

Fields follow the shared directory schema (naam, slug, provincie, plaats, adres, telefoon, website, status, kenmerken, …). See `scrape_listings.py` for writers.

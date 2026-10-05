# Metaalhandel-gids.nl (Astro)

Dutch psychologist / practice directory — Django-overzicht family, scaffolded from basisschool-gids and scrubbed for metaalhandels.

## Run

```bash
cd sites/metaalhandel-gids
npm install
npm run dev
```

Dev server: [http://127.0.0.1:43851](http://127.0.0.1:43851)

## Build

```bash
npm run build
npm run preview
```

## Data

- `src/content/metaalhandels/*.json` — scraped + triage (separate scrape process)
- `src/data/cities.json` — Group A stub (Semrush NL volumes TBD)
- `src/lib/city-intents.ts` — titles/descriptions + city H2 stubs (fill after Semrush)
- `migration/semrush/` — place NL exports here (do not reuse basisschool/keramiek CSVs)
- `migration/assets/heroes/` — city heroes (synced to `public/heroes` on prebuild)

**Scrape vs Semrush:** scrape = listing inventory on the live site; Semrush = KD + volume for keywords/cities.

## Design

Blue CSS tokens (porcelain + cobalt) in `src/styles/global.css`. Brand mark: **Zwembad**`1`**.nl**. See `migration/design/`.

## Hosting

GitHub: `bruske0102/sites-metaalhandel-gids` (site-only push at repo root). Worker name: `metaalhandel-gids`.  
CF **Root directory = empty**. See `migration/GO_LIVE_NOW.md` for CF Worker + Builds, Email Routing, domain, GSC+Bing.

## Locked decisions

See `migration/DECISIONS.md` — brand Metaalhandel-gids.nl, metaalhandels only (no coaches/lifestyle junk), SBO-equivalent N/A.

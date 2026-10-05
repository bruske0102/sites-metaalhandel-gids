# Metaalhandel-gids.nl — beginner go-live

1. **GitHub** — `bruske0102/sites-metaalhandel-gids` `main` has site at repo root (not monorepo).
2. **CF Worker Builds** — Worker name `metaalhandel-gids`, Root directory **empty**, `npm ci && npm run build`, `npx wrangler deploy`.
3. **Visit** workers.dev — confirm Astro metaalhandel site (blue), not Django / other niche.
4. **Email Routing** — `info@metaalhandel-gids.nl` before domain attach (`playbook/CF_EMAIL_ROUTING.md`).
5. **Custom domain** — attach `metaalhandel-gids.nl` only after Visit + email OK.
6. **GSC + Bing** — submit `https://metaalhandel-gids.nl/sitemap-index.xml`.

See also: [`GO_LIVE_NOW.md`](./GO_LIVE_NOW.md)

## Local

- Preview (agent): `http://127.0.0.1:43851/`
- Verify: `npm run verify:golive` (optional; needs running preview)

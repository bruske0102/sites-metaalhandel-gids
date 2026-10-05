/**
 * Semrush NL city/intent research for Metaalhandel (2026-10-04).
 * Volumes from phrase_these database=nl. Do not invent numbers.
 * A-plus threshold = local vol ≥200.
 */
import { listingCount } from "./nl-count";

export type CityIntentFlags = {
  volume: number;
  kd?: number;
  primaryPhrase: string;
};

/** Keyed by plaats slug. */
export const CITY_INTENTS: Record<string, CityIntentFlags> = {
  "amsterdam": { volume: 390, kd: 8, primaryPhrase: "oud ijzer amsterdam" },
  "den-haag": { volume: 390, kd: 20, primaryPhrase: "oud ijzer den haag" },
  "utrecht": { volume: 390, kd: 14, primaryPhrase: "oud ijzer utrecht" },
  "utrecht-gemeente": { volume: 390, kd: 14, primaryPhrase: "oud ijzer utrecht" },
  "rotterdam": { volume: 320, kd: 25, primaryPhrase: "oud ijzer rotterdam" },
  "eindhoven": { volume: 260, kd: 23, primaryPhrase: "oud ijzer eindhoven" },
  "emmen": { volume: 260, kd: 18, primaryPhrase: "oud ijzer emmen" },
  "enschede": { volume: 260, kd: 11, primaryPhrase: "oud ijzer enschede" },
};

export const INTENT_BLOG_LINKS = {
  prijzen: { href: "/blog/oud-ijzer-prijs/", label: "Dagprijs oud ijzer" },
  ophalen: { href: "/blog/oud-ijzer-ophalen/", label: "Oud ijzer ophalen" },
  kiezen: { href: "/blog/metaalhandel-kiezen/", label: "Metaalhandel kiezen" },
} as const;

export function cityIntent(plaatsSlug: string): CityIntentFlags | undefined {
  return CITY_INTENTS[plaatsSlug];
}

export function isHighTrafficCity(plaatsSlug: string): boolean {
  const row = CITY_INTENTS[plaatsSlug];
  return Boolean(row && row.volume >= 200);
}

export function cityPageTitle(opts: {
  stad: string;
  plaatsSlug: string;
  n: number;
  aPlus?: boolean;
}): string {
  const { stad, plaatsSlug, n } = opts;
  const intent = CITY_INTENTS[plaatsSlug];
  if (n <= 0) return `Metaalhandel ${stad}`;
  if (intent && intent.volume >= 200) {
    return `Metaalhandel ${stad}: oud ijzer, schroot & adressen`;
  }
  return `Metaalhandel ${stad}: ${listingCount(n)} met adres`;
}

export function cityPageDescription(opts: {
  stad: string;
  plaatsSlug: string;
  n: number;
  provincieNaam: string;
  aPlus?: boolean;
}): string {
  const { stad, n, provincieNaam } = opts;
  return `Vergelijk ${listingCount(n)} in ${stad} (${provincieNaam}): adres, telefoon en openingstijden.`;
}

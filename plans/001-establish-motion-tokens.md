# 001 — Establish crisp motion tokens

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: LOW
- **Category**: Cohesion & tokens / Easing & duration
- **Estimated scope**: 1 file, about 30 CSS lines

## Problem

`index.html` keeps colors and typography in `:root`, but every motion value is hand-written. There is no shared easing or duration scale:

```css
/* index.html:11-24 — current */
:root {
  --ink: #1a1b2e;
  --ink-80: #2a2b42;
  --ink-60: #5a5b72;
  --ink-40: #9a9ba8;
  --ink-20: #d4d5dc;
  --paper: #faf8f4;
  --white: #ffffff;
  --rule: rgba(26,27,46,0.08);
  --accent: #4f46e5;
  --sans: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  --serif: "Instrument Serif", Georgia, serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

The mobile-menu morph and drawer use the browser's implicit `ease`, even though one is an on-screen morph and the other is entering/exiting UI:

```css
/* index.html:668-669 — exact current declarations */
transition: transform 0.3s, opacity 0.3s;
transform-origin: center;

/* index.html:689 — exact current declaration */
transition: opacity 0.3s, transform 0.3s;
```

This makes later fixes likely to introduce more near-duplicate timings and curves.

## Target

Add the audit's exact strong curves and a small duration scale to the existing `:root` block:

```css
/* target additions inside :root */
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
--duration-press: 160ms;
--duration-small: 200ms;
--duration-ui: 250ms;
--duration-drawer: 300ms;
```

Use the tokens on the menu and avoid collapsing the middle bar to zero scale:

```css
/* target */
.nav-hamburger span {
  transition:
    transform var(--duration-ui) var(--ease-in-out),
    opacity var(--duration-small) var(--ease-out);
  transform-origin: center;
}

.nav-hamburger.open span:nth-child(2) {
  opacity: 0;
  transform: scaleX(0.95);
}

.mobile-nav {
  transition:
    opacity var(--duration-drawer) var(--ease-drawer),
    transform var(--duration-drawer) var(--ease-drawer);
}

.mobile-nav a {
  transition: color var(--duration-small) ease;
}
```

The 250ms hamburger morph stays below the 300ms UI ceiling. The 300ms drawer stays inside the audit's 200–500ms modal/drawer budget.

## Repo conventions to follow

- All styles live in the single `<style>` block in `index.html`; do not create a second stylesheet.
- Existing design tokens already live in `index.html:11-24`; append motion tokens there.
- Keep color-only hover transitions on CSS `ease`; use the strong custom curves for movement and entrances.

## Steps

1. In `index.html`, append the seven target motion variables after `--mono` inside `:root`.
2. Replace the hamburger's implicit 300ms transitions with the exact tokenized target above.
3. Replace `.nav-hamburger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }` with the exact nonzero `scaleX(0.95)` target above.
4. Replace the mobile drawer's implicit 300ms transitions with `--duration-drawer` and `--ease-drawer`.
5. Replace the mobile-link color transition with `color var(--duration-small) ease`.
6. Do not bulk-replace every transition yet; Plan 005 changes the remaining interactions while converting layout-property animation to transforms.

## Boundaries

- Do NOT change JavaScript or HTML markup.
- Do NOT alter colors, typography, spacing, menu structure, or breakpoints.
- Do NOT add a CSS framework or dependency.
- Do NOT introduce additional curves or durations beyond the seven values above.
- If the excerpts no longer match commit `360d60b`, STOP and report drift instead of improvising.

## Verification

- **Mechanical**: run `git diff --check` and confirm no errors. Run `rg -n -- '--ease-|--duration-' index.html` and confirm all seven tokens exist exactly once in `:root`. Run `rg -n "scaleX\\(0\\)" index.html`; it must return no matches.
- **Feel check**: serve the directory with `python3 -m http.server 4173`, open `http://127.0.0.1:4173/index.html`, switch DevTools to a mobile viewport, and open/close the menu repeatedly.
  - The drawer must start fast and settle cleanly rather than using the browser's weak default curve.
  - The hamburger morph must be smooth and non-bouncy.
  - At 10% playback speed, opacity and transform must finish without a late tail.
- **Done when**: all seven shared values exist, the menu uses them, and no implicit movement easing remains in the hamburger or drawer.

# 005 — Make interaction feedback compositor-safe

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: MEDIUM
- **Category**: Performance / Accessibility / Physicality
- **Estimated scope**: 1 file, about 100 CSS/JavaScript lines

## Problem

Remaining CSS feedback animates layout properties and movement hover rules are not positively gated to a fine pointer.

```css
/* index.html:59-64 — exact current rule */
.nav-links a::after {
  content: ''; position: absolute;
  left: 0; bottom: -4px; height: 1px; width: 0;
  background: currentColor;
  transition: width 0.3s ease;
}

/* index.html:66 — exact current rule */
.nav-links a:hover::after { width: 100%; }

/* index.html:76-84 — exact current rule */
.nav-cta::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  transition: left 0.6s ease;
}
.nav-cta:hover::before { left: 100%; }
```

The same `left` shimmer appears at `index.html:147-152` and `index.html:479-484`. Process rows animate padding:

```css
/* index.html:350 — exact current declaration */
transition: padding 0.4s;

/* index.html:353 — exact current rule */
.step:hover { padding-left: 12px; }
```

The progress bar animates width on every scroll update:

```js
/* index.html:1315-1318 — current */
gsap.to('#scrollProg', {
  width: '100%',
  ease: 'none',
  scrollTrigger: { start: 0, end: 'max', scrub: 0.1 }
});
```

Client logos animate a paint-heavy filter, while pressable elements have no explicit press feedback:

```css
/* index.html:217-220 — exact current declarations */
filter: grayscale(1) contrast(1.04);
opacity: 0.5;
mix-blend-mode: multiply;
transition: filter 0.35s ease, opacity 0.35s ease;

/* index.html:222 — exact current rule */
.marquee-track .client-logo:hover img { filter: grayscale(0); opacity: 1; }
```

## Target

Only animate `transform` and `opacity` for movement. Gate hover behavior with the audit's exact capability query and add the audit's exact press feedback.

Navigation underline:

```css
/* target */
.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 100%;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform var(--duration-ui) var(--ease-out);
}
```

All three shimmer pseudo-elements must start and move via transform:

```css
/* target pattern for .nav-cta::before, .btn.primary::before, .cta-btn::before */
top: 0;
left: 0;
width: 100%;
height: 100%;
transform: translateX(-100%);
transition: transform var(--duration-ui) var(--ease-out);
```

Use one positive hover media query for movement and hover-only visual changes:

```css
/* target */
@media (hover: hover) and (pointer: fine) {
  .nav-links a:hover { color: var(--ink); }
  .nav-links a:hover::after { transform: scaleX(1); }
  .nav-cta:hover { transform: translateY(-1px); background: var(--ink-80); }
  .nav-cta:hover::before,
  .btn.primary:hover::before,
  .cta-btn:hover::before { transform: translateX(100%); }
  .btn.primary:hover { transform: translateY(-1px); background: var(--ink-80); }
  .btn.ghost:hover { color: var(--accent); }
  .btn:hover .arrow { transform: translateX(4px); }
  .service:hover { background: var(--white); }
  .marquee-track .client:hover { color: var(--ink); }
  .marquee-track .client-logo:hover img { opacity: 1; }
  .cta-btn:hover { transform: translateY(-2px); }
  .cta-btn--wa:hover { background: var(--ink); color: var(--white); }
  .foot-grid ul a:hover,
  .mobile-nav a:hover { color: var(--accent); }
}
```

Add press feedback outside the hover query so touch and keyboard-activated controls receive it:

```css
/* target */
.nav-cta,
.btn,
.cta-btn,
.nav-hamburger,
.mobile-nav a {
  transition-property: transform, background-color, color;
  transition-duration: var(--duration-press), var(--duration-small), var(--duration-small);
  transition-timing-function: var(--ease-out), ease, ease;
}

.nav-cta:active,
.btn.primary:active,
.btn.ghost:active,
.cta-btn:active,
.cta-btn--wa:active,
.nav-hamburger:active,
.mobile-nav a:active {
  transform: scale(0.97);
}
```

Preserve component-specific display/layout declarations. If the grouped transition rule conflicts with a more specific component rule, merge these three transition properties into that component rule instead of duplicating `transition` shorthands. Place the active selector block after the fine-pointer hover block. The explicit `.btn.primary:active`, `.btn.ghost:active`, and `.cta-btn--wa:active` selectors are required so more-specific hover rules cannot win while a control is pressed.

Remove process-row movement entirely; the rows are informational, not interactive:

```css
/* target */
.step {
  /* retain layout/padding; remove transition: padding */
}
/* delete .step:hover */
```

Make logo hover opacity-only:

```css
/* target */
.marquee-track .client-logo img {
  /* retain dimensions/layout */
  filter: grayscale(1) contrast(1.04);
  opacity: 0.5;
  transition: opacity var(--duration-small) ease;
}
```

Make scroll progress transform-only:

```css
/* target */
.scroll-prog {
  /* retain position, dimensions, color, and z-index */
  width: 100%;
  transform: scaleX(0);
  transform-origin: left center;
}
```

```js
/* target */
gsap.to('#scrollProg', {
  transform: 'scaleX(1)',
  ease: 'none',
  scrollTrigger: { start: 0, end: 'max', scrub: 0.1 }
});
```

## Repo conventions to follow

- Requires the exact tokens from Plan 001.
- Plans 003 and 004 remove hero width animation, cursor sizing, and pointer-driven effects before this cleanup.
- Keep constant scroll progress linear (`ease: 'none'`), matching the audit's linear rule for constant motion.

## Steps

1. Confirm Plans 001, 003, and 004 are complete.
2. Convert the nav underline from animated width to `scaleX` using the exact target.
3. Convert all three shimmer effects from `left` to `translateX`; keep WhatsApp's existing `::before { display: none; }` exemption.
4. Move all movement hover selectors into one `(hover: hover) and (pointer: fine)` query. Remove their old global duplicates.
5. Replace the old coarse-touch hover override block; it should no longer be necessary once hover behavior is positively gated.
6. Add the exact specific active selector block after the hover media query. Use `scale(0.97)` with `160ms` `--ease-out` transition behavior for navigation CTA, both button variants, both CTA button variants, hamburger, and mobile links.
7. Delete process-row padding animation and `.step:hover` movement.
8. Remove filter interpolation from client logos; retain static grayscale and animate opacity only.
9. Change scroll progress from `width: 0 → 100%` to `scaleX(0 → 1)` in CSS and GSAP.
10. Search all transition declarations. Confirm no remaining transition animates `width`, `height`, `left`, `padding`, `margin`, `top`, or `filter`.

## Boundaries

- Do NOT reintroduce pointermove JavaScript removed by Plan 004.
- Do NOT change element dimensions, padding, grid layout, breakpoints, colors, or destinations.
- Do NOT remove the scroll progress indicator for no-preference users.
- Do NOT animate `transition: all`.
- Do NOT use a press scale outside the audit's 0.95–0.98 range; use exactly `0.97` and `160ms`.
- If prerequisites changed a cited selector unexpectedly, STOP and report drift.

## Verification

- **Mechanical**: run `git diff --check`. Run `rg -n "transition:[^;]*(width|height|left|padding|margin|top|filter)" index.html`; it must return no matches. Run `rg -U "gsap\\.to\\('#scrollProg',[\\s\\S]*?width:" index.html`; it must return no matches. Run `rg -U "gsap\\.to\\('#scrollProg',[\\s\\S]*?transform: 'scaleX\\(1\\)'" index.html` and confirm one match. Run `rg -n "@media \\(hover: hover\\) and \\(pointer: fine\\)|scale\\(0\\.97\\)" index.html` and confirm both patterns exist.
- **Feel check**: serve with `python3 -m http.server 4173`.
  - At 10% playback speed, underlines and sheens must move without changing layout boxes.
  - Hovering process rows must not shift content.
  - Press and hold each CTA on desktop and touch emulation; it must compress subtly to 97% and retarget smoothly when released.
  - In touch emulation, no hover lift, arrow translation, underline sweep, or sheen may stick after a tap.
  - Scroll the page while recording Performance; the progress bar must update through transform, not layout width.
- **Done when**: remaining interaction motion uses transform/opacity, hover movement is fine-pointer-only, and every primary pressable has subtle 160ms press feedback.

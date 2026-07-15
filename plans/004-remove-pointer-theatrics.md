# 004 — Remove high-frequency pointer theatrics

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: HIGH
- **Category**: Purpose & frequency / Performance / Cohesion
- **Estimated scope**: 1 file, about 170 lines removed or simplified

## Problem

Four decorative systems run on frequent pointer input and conflict with the restrained consultancy presentation.

The custom cursor starts a page-lifetime animation loop:

```js
/* index.html:1165-1177 — current excerpt */
function raf() {
  x += (tx - x) * 0.2; y += (ty - y) * 0.2;
  cur.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
  requestAnimationFrame(raf);
}
raf();
```

Magnetic buttons create two 600ms tweens per `pointermove` and 800ms elastic resets:

```js
/* index.html:1326-1338 — exact current excerpt */
const reset = () => {
  gsap.to(wrap, { x: 0, y: 0, duration: 0.8, ease: 'elastic.out(1, 0.4)' });
  gsap.to(child, { x: 0, y: 0, duration: 0.8, ease: 'elastic.out(1, 0.4)' });
};
wrap.addEventListener('pointermove', e => {
  const r = wrap.getBoundingClientRect();
  const x = e.clientX - r.left - r.width / 2;
  const y = e.clientY - r.top - r.height / 2;
  gsap.to(wrap, { x: x * strength, y: y * strength, duration: 0.6, ease: 'power3.out' });
  gsap.to(child, { x: x * strength * 0.5, y: y * strength * 0.5, duration: 0.6, ease: 'power3.out' });
});
```

Service cards repeat the same pattern with 3D rotation:

```js
/* index.html:1422-1436 — exact current excerpt */
const reset = () => gsap.to(card, { rotationY: 0, rotationX: 0, duration: 0.8, ease: 'elastic.out(1, 0.5)' });
card.addEventListener('pointermove', e => {
  const r = card.getBoundingClientRect();
  const px = (e.clientX - r.left) / r.width - 0.5;
  const py = (e.clientY - r.top) / r.height - 0.5;
  gsap.to(card, {
    rotationY: px * 8,
    rotationX: -py * 8,
    transformPerspective: 900,
    duration: 0.6,
    ease: 'power2.out',
  });
});
```

The CTA headline performs a layout read and creates a tween for every character on every pointer event:

```js
/* index.html:1463-1478 — exact current excerpt */
h.addEventListener('pointermove', e => {
  chars.forEach(c => {
    const r = c.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const dist = Math.hypot(e.clientX - cx, e.clientY - cy);
    const maxDist = 160;
    if (dist < maxDist) {
      gsap.to(c, { y: (1 - dist / maxDist) * -14, duration: 0.4, ease: 'power2.out' });
    } else {
      gsap.to(c, { y: 0, duration: 0.6, ease: 'power2.out' });
    }
  });
});
```

## Target

Remove all four systems. Keep the native cursor, static cards, stable CTA headline, and normal button hit targets. This is deliberately a deletion plan: these interactions are encountered tens or hundreds of times and do not explain state or spatial relationships.

Delete these CSS blocks/declarations:

```css
/* remove entirely */
.service.tilt-ready { transform-style: preserve-3d; will-change: transform; }
.service.tilt-ready > * { transform: translateZ(30px); }
.cursor { /* entire block */ }
.cursor.hover { /* entire rule */ }
.magnetic { display: inline-block; will-change: transform; }
.magnetic > * { display: inline-block; will-change: transform; }
.cta-h .char { display: inline-block; will-change: transform; }
@media (hover: none) { .cursor { display: none; } }
```

Delete the cursor element:

```html
<!-- remove from index.html:846 -->
<div class="cursor" id="cursor"></div>
```

Remove the `magnetic` class while preserving wrapper elements and layout:

Apply all four exact opening-tag replacements without changing descendants or closing tags:

```html
<!-- index.html:901 — current -->
<span class="magnetic">
<!-- target -->
<span>

<!-- index.html:904 — current -->
<span class="magnetic">
<!-- target -->
<span>

<!-- index.html:1098 — current -->
<span class="magnetic" style="display: inline-block;">
<!-- target -->
<span style="display: inline-block;">

<!-- index.html:1101 — current -->
<span class="magnetic" style="display: inline-block;">
<!-- target -->
<span style="display: inline-block;">
```

Preserve every nested anchor and all closing tags verbatim.

Delete these complete JavaScript sections:

- `// ── Custom cursor`
- `// ── Magnetic buttons (desktop only)`
- `// ── Service card 3D tilt (desktop only)`
- `// ── CTA headline char-by-char hover wave (desktop only)`

After Plan 003 has removed the scramble, these deletions leave no `isTouch` consumer. Delete:

```js
const isTouch = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
```

## Repo conventions to follow

- Prefer native HTML/CSS interaction over page-lifetime JavaScript loops.
- Preserve the existing static card background hover; Plan 005 gates and retimes that simple feedback.
- Preserve wrapper spans to avoid layout changes. Only remove their dead `magnetic` class.

## Steps

1. Confirm Plan 003 is complete and `isTouch` is no longer used by the scramble.
2. Remove the cursor `<div>`, cursor CSS, touch cursor media rule, and full cursor IIFE.
3. Remove `.magnetic` CSS and the `magnetic` class from all four wrappers; retain the wrappers and any inline display style.
4. Delete the full magnetic-button JavaScript block.
5. Remove both `.service.tilt-ready` rules and the full service-card tilt JavaScript block.
6. Remove `.cta-h .char` and the full CTA headline character-wrapping/wave IIFE. The original heading text remains unchanged in HTML, so no replacement markup is needed.
7. Delete `isTouch` after verifying `rg -n "isTouch" index.html` finds only the declaration.
8. Remove the now-obsolete `.magnetic { will-change: auto !important; }` declaration from the coarse-touch media block; Plan 005 replaces that media strategy completely.

## Boundaries

- Requires Plan 003 first.
- Do NOT remove normal CSS hover color/background feedback, CTA arrows, client-logo feedback, marquee motion, or scroll reveals.
- Do NOT alter copy, destinations, card structure, CTA structure, or responsive layout.
- Do NOT replace any deleted effect with another pointer listener or animation library.
- Do NOT add `cursor: none`.
- If any complete block cannot be identified unambiguously, STOP and report drift.

## Verification

- **Mechanical**: run `git diff --check`. Run `rg -n "cursor|magnetic|tilt-ready|isTouch|pointermove|elastic\\.out|className = 'char'" index.html`; there must be no matches except ordinary CSS `cursor: pointer` on the hamburger if retained.
- **Feel check**: serve with `python3 -m http.server 4173`.
  - Move rapidly across buttons, service cards, and the CTA heading. Nothing should chase, tilt, lag, or bounce.
  - The browser's native cursor must remain visible and responsive.
  - Buttons and cards must remain in their original layout with no jump caused by removing transforms.
  - Use Chrome Performance for a five-second pointer sweep; there should be no page-lifetime cursor rAF and no pointermove-driven GSAP work.
- **Done when**: all content remains stable under pointer movement and the four decorative systems leave no CSS, markup hook, or JavaScript listener behind.

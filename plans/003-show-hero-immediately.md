# 003 — Show the hero immediately

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: HIGH
- **Category**: Purpose & frequency / Easing & duration
- **Estimated scope**: 1 file, about 80 lines removed or simplified

## Problem

Critical hero content starts hidden in CSS:

```css
/* index.html:101 — exact current declaration */
opacity: 0;

/* index.html:105-107 — exact current rule */
.hero-eyebrow::before {
  content: ''; display: inline-block; width: 0; height: 1px; background: var(--ink-60);
}

/* index.html:116 — exact current rule */
.hero-h1 .line span { display: inline-block; transform: translateY(110%); }

/* index.html:133 — exact current declaration */
opacity: 0;

/* index.html:136 — exact current rule */
.hero-ctas { display: flex; gap: 14px; opacity: 0; }
```

A long timeline then reveals it:

```js
/* index.html:1190-1200 — current */
const heroTl = gsap.timeline({ delay: 0.3, defaults: { ease: 'expo.out' } });
heroTl
  .to('#heroEyebrow', { opacity: 1, duration: 0.6 })
  .to('#heroEyebrow .line-anim', { width: 40, duration: 0.8 }, '<')
  .to('#heroH1 .line span', { y: 0, duration: 1.3, stagger: 0.12 }, '-=0.4')
  .to('#heroSub', { opacity: 1, y: 0, duration: 0.9 }, '-=0.6')
  .to('#heroCtas', { opacity: 1, y: 0, duration: 0.8 }, '-=0.5')
  .from('#heroSymbol', { opacity: 0, scale: 1.1, duration: 1.6 }, '-=1.4');
```

Browser sampling showed the headline still moving around 1.5s and the CTA nearly invisible until about 1.9s. As the CTA becomes readable, the key word is replaced by random characters for roughly 2.87s:

```js
/* index.html:1353-1375 — current excerpts */
const chars = '!@#$%^&*<>-_=+[]{}|;:,./?abcdefghijklmnopqrstuvwxyz';
const total = 40;
const int = setInterval(() => {
  /* replaces the word character by character */
}, 70);
setTimeout(scramble, 2200);
if (!isTouch) el.parentElement.addEventListener('pointerenter', scramble);
```

This delays comprehension and action on the landing page's most important screen.

## Target

The entire hero message and both CTAs must be readable at first paint. Remove the entrance timeline and the scramble behavior rather than substituting another decorative animation.

Use these static styles:

Change only the following declarations; preserve every unlisted declaration in each existing rule:

```css
/* exact target declarations */
.hero-eyebrow { opacity: 1; }

.hero-eyebrow::before {
  content: '';
  display: inline-block;
  width: 40px;
  height: 1px;
  background: var(--ink-60);
}

.hero-h1 .line span {
  display: inline-block;
  transform: none;
}

.hero-sub { opacity: 1; }

.hero-ctas {
  display: flex;
  gap: 14px;
  opacity: 1;
}
```

Simplify the eyebrow and headline markup:

```html
<!-- target -->
<div class="hero-eyebrow" id="heroEyebrow">
  <span>Software · IA · Sistemas a medida</span>
</div>

<!-- target excerpt -->
<span class="line"><span>resuelven <em>problemas</em>.</span></span>
```

Delete the complete `// ── Hero entrance` timeline and the complete `// ── Text scramble on hero word` IIFE. Delete the now-unused `.scramble` CSS rule and `.hero-h1 .line span { white-space: nowrap; }` override only if the earlier general mobile/desktop wrapping rules still behave correctly; otherwise keep the wrapping rule but remove all scramble-specific declarations.

## Repo conventions to follow

- This is a static landing page; critical content should be present without JavaScript.
- Preserve the existing editorial typography and the static 40px eyebrow rule.
- Keep hero-symbol scroll parallax for no-preference users; Plan 002 handles its reduced-motion branch.

## Steps

1. Make `.hero-eyebrow`, `.hero-sub`, and `.hero-ctas` statically opaque.
2. Remove the initial `translateY(110%)` from hero title spans.
3. Give `.hero-eyebrow::before` a static `width: 40px`.
4. Remove the redundant `<span class="line-anim"></span>` from the eyebrow markup.
5. Remove `class="scramble"` and `id="scrambleWord"` from the word “problemas”.
6. Delete the `.scramble` CSS block and any width reservation used only by the scramble.
7. Delete the entire GSAP hero entrance timeline.
8. Delete the entire text-scramble IIFE, including its `requestAnimationFrame`, interval, timeout, and hover listener.
9. Reload with JavaScript disabled and confirm the complete hero remains visible.

## Boundaries

- Do NOT change hero copy, typography, spacing, logo placement, links, or CTA destinations.
- Do NOT remove hero-symbol scroll parallax; accessibility handling belongs to Plan 002.
- Do NOT replace the removed effects with another keyframe, timer, typewriter, or character effect.
- Do NOT remove `isTouch` yet; Plan 004 removes the remaining consumers and then deletes it.
- If the cited hero or scramble blocks differ from commit `360d60b`, STOP and report drift.

## Verification

- **Mechanical**: run `git diff --check`. Run `rg -n "heroTl|scrambleWord|function scramble|setTimeout\\(scramble|line-anim" index.html`; it must return no matches.
- **Feel check**: serve with `python3 -m http.server 4173`, then test desktop and 375px mobile widths.
  - At a cold reload, the eyebrow, all headline lines, supporting paragraph, and both CTAs must be visible immediately.
  - Wait at least six seconds; “problemas” must never change.
  - Move the pointer over the headline; no character replacement may occur.
  - Disable JavaScript and reload; the same critical content must remain visible.
- **Done when**: first paint communicates the complete proposition and exposes both actions without waiting for animation or JavaScript.

# 007 — Restore refined hero letter motion

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: LOW
- **Category**: Purpose & frequency / Easing & duration / Accessibility
- **Estimated scope**: 1 source file, about 55 CSS/HTML/JavaScript lines

## Problem

The completed cleanup made the hero fully static:

```css
/* index.html:119-120 — current */
.hero-h1 .line { display: block; overflow: hidden; }
.hero-h1 .line span { display: inline-block; transform: none; }
```

```html
<!-- index.html:923-927 — current -->
<h1 class="hero-h1" id="heroH1">
  <span class="line"><span>Construimos</span></span>
  <span class="line"><span>sistemas que</span></span>
  <span class="line"><span>resuelven <em>problemas</em>.</span></span>
</h1>
```

The user explicitly wants two pieces of personality restored: the headline lines entering from below and the word “problemas” scrambling. The previous version delayed critical content and automatically scrambled the word for almost three seconds, so it must not be restored verbatim.

## Target

### Headline entrance

Use an interruptible CSS transition with `@starting-style`. Unsupported browsers render the final readable state immediately, and reduced-motion users receive no positional animation.

```css
/* target */
.hero-h1 .line { display: block; overflow: hidden; }

.hero-h1 .line span {
  display: inline-block;
  transform: translateY(0);
  transition: transform 800ms var(--ease-out);
}

.hero-h1 .line:nth-child(2) span { transition-delay: 60ms; }
.hero-h1 .line:nth-child(3) span { transition-delay: 120ms; }

@starting-style {
  .hero-h1 .line span { transform: translateY(110%); }
}
```

The delay between adjacent lines is exactly 60ms, within the audit's 30–80ms decorative stagger range. Only the headline animates: eyebrow, supporting paragraph, and CTAs remain visible immediately.

Extend the existing reduced-motion media query with:

```css
/* target inside @media (prefers-reduced-motion: reduce) */
.hero-h1 .line span {
  transform: none;
  transition: none;
}
```

### Hover-only scramble

Change only the emphasized word markup:

```html
<!-- target -->
<span class="line"><span>resuelven <em class="scramble" id="scrambleWord" aria-label="problemas">problemas</em>.</span></span>
```

Add this CSS near the hero rules:

```css
/* target */
.scramble {
  display: inline-block;
  min-width: 5ch;
  white-space: nowrap;
}
```

Add the following JavaScript immediately after the `motionQuery`/`reduceMotion` setup and before the nav ScrollTrigger. It runs only for no-preference users with a fine pointer, never automatically:

```js
/* target */
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

if (!reduceMotion && finePointer) {
  const scrambleWord = document.getElementById('scrambleWord');
  const originalWord = scrambleWord.textContent;
  const scrambleChars = '!@#$%^&*<>-_=+[]{}|;:,./?abcdefghijklmnopqrstuvwxyz';
  const originalWidth = scrambleWord.getBoundingClientRect().width;
  let scrambleTween;

  scrambleWord.style.width = `${originalWidth}px`;
  scrambleWord.style.textAlign = 'left';

  scrambleWord.closest('.line').addEventListener('pointerenter', () => {
    scrambleTween?.kill();
    const state = { progress: 0 };

    scrambleTween = gsap.to(state, {
      progress: 1,
      duration: 0.6,
      ease: 'power2.out',
      onUpdate: () => {
        const revealed = Math.floor(state.progress * originalWord.length);
        scrambleWord.textContent = [...originalWord].map((character, index) => {
          if (index < revealed || character === ' ') return character;
          return scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
        }).join('');
      },
      onComplete: () => {
        scrambleWord.textContent = originalWord;
        scrambleTween = undefined;
      }
    });
  });
}
```

The 600ms hover-only treatment is a rare marketing flourish, not control feedback. It is short enough to restore readability promptly and is drastically reduced from the previous ~2.87s automatic effect.

## Repo conventions to follow

- Motion tokens already live in `index.html:24-30`; reuse `--ease-out`.
- The project already uses GSAP for dynamic motion; do not add another dependency.
- The current reduced-motion source of truth is `reduceMotion` plus the final CSS media query.
- Preserve the current immediate visibility of `.hero-eyebrow`, `.hero-sub`, and `.hero-ctas`.

## Steps

1. Add the CSS transition, 60ms adjacent stagger, and `@starting-style` block exactly as specified.
2. Add the reduced-motion override inside the existing media query.
3. Add `class="scramble"`, `id="scrambleWord"`, and `aria-label="problemas"` to the existing `<em>` without changing the word or surrounding punctuation.
4. Add the `.scramble` width-preservation rule.
5. Add the exact fine-pointer/no-preference GSAP block after the motion preference constants.
6. Confirm there is no timeout, interval, page-load invocation, or touch listener for the scramble.
7. Keep all completed plan statuses unchanged; mark this plan `DONE` only after every verification passes.

## Boundaries

- Do NOT hide or animate the eyebrow, supporting paragraph, CTAs, mobile logo, or hero symbol.
- Do NOT add an initial delay before the line entrance.
- Do NOT restore the old automatic `setTimeout(scramble, 2200)` behavior.
- Do NOT use `setInterval`, `requestAnimationFrame`, keyframes, or pointermove listeners.
- Do NOT run the scramble on touch or under `prefers-reduced-motion: reduce`.
- Do NOT change hero copy, typography, spacing, wrapping rules, or CTA destinations.
- Do NOT add dependencies.
- If the current excerpts no longer match the post-plan implementation, STOP and report drift instead of improvising.

## Verification

- **Mechanical**: run `git diff --check`. Parse the inline script with Node's `vm.Script`. Run `rg -n "setTimeout\\(scramble|setInterval|requestAnimationFrame|pointermove" index.html`; it must return no matches related to this feature. Run `rg -n "@starting-style|stagger|transition-delay: 60ms|transition-delay: 120ms|duration: 0\\.6|scrambleWord" index.html` and confirm every target exists.
- **Feel check**: serve with `python3 -m http.server 4173` and test desktop plus 375px mobile.
  - On cold load, the three headline lines must rise from their clipped containers with 60ms between adjacent starts.
  - Eyebrow, paragraph, and CTAs must be visible immediately and must not move.
  - Wait six seconds without interaction; “problemas” must remain unchanged.
  - On a fine-pointer hover over the final line, “problemas” must scramble once and return exactly to the original within 600ms.
  - Re-enter repeatedly; the effect must restart cleanly without overlapping tweens or changing line width.
  - On touch emulation, hover must not trigger the effect.
  - With reduced motion enabled, the headline must be static and immediately visible; scramble must never run.
  - Disable JavaScript and reload; the headline and CTAs must remain readable, and the CSS entrance may run only if the browser supports `@starting-style`.
- **Done when**: both requested hero effects are restored in their refined form without automatic obfuscation, CTA delay, touch hover, width shift, or reduced-motion movement.

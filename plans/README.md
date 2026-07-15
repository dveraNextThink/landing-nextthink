# Animation improvement plans

Plans are stamped against commit `360d60b`. They intentionally modify only `index.html` when executed; the planning pass itself did not modify source code.

## Plan index

| # | Plan | Severity | Status | Dependencies |
|---|---|---|---|---|
| 001 | [Establish crisp motion tokens](001-establish-motion-tokens.md) | LOW | DONE | — |
| 002 | [Respect reduced motion everywhere](002-respect-reduced-motion.md) | HIGH | DONE | 003, 004, 005 |
| 003 | [Show the hero immediately](003-show-hero-immediately.md) | HIGH | DONE | — |
| 004 | [Remove high-frequency pointer theatrics](004-remove-pointer-theatrics.md) | HIGH | DONE | 003 |
| 005 | [Make interaction feedback compositor-safe](005-make-interactions-compositor-safe.md) | MEDIUM | DONE | 001, 003, 004 |
| 006 | [Stagger grouped reveals](006-stagger-grouped-reveals.md) | LOW | DONE | 002 |
| 007 | [Restore refined hero letter motion](007-restore-refined-hero-letter-motion.md) | LOW | DONE | 001, 002, 003 |

## Recommended execution order

1. **001** — establish the easing and duration vocabulary used by later CSS changes.
2. **003** — make critical hero content immediate and remove the scramble before deleting the shared touch flag.
3. **004** — remove cursor, magnetic, tilt, and character-wave systems; depends on 003 so `isTouch` can be deleted safely.
4. **005** — convert the remaining interaction layer to transform/opacity, add press feedback, and positively gate hover motion.
5. **002** — add the final reduced-motion branch after 005 so its media-query overrides suppress every remaining hover/press transform while retaining color and opacity feedback.
6. **006** — apply the final 60ms group stagger inside the reduced/no-preference reveal structure created by 002.
7. **007** — restore the requested headline entrance and hover-only scramble without regressing first-paint or reduced-motion behavior.

Do not run these plans concurrently: every plan edits the same source file. Execute and verify one plan at a time.

## Coverage

- Broken `prefers-reduced-motion` behavior: **002**
- Delayed hero and repeating text scramble: **003**
- CTA character-wave layout work: **004**
- Magnetic buttons, service tilt, elastic personality mismatch, and perpetual custom cursor: **004**
- Layout-property transitions, ungated hover motion, paint-heavy logo transition, and scroll-progress width animation: **005**
- Missing button press feedback: **005**
- Missing motion tokens and weak mobile-menu easing: **001**
- Simultaneous stats reveal and slow service stagger: **006**
- Refined hero line entrance and hover-only word scramble: **007**

## Status workflow

Change a plan from `TODO` to `IN PROGRESS` only when execution starts, and to `DONE` only after its full mechanical and feel-check verification passes. Update the matching row in this file at the same time.

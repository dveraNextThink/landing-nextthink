# 006 — Stagger grouped reveals

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: LOW
- **Category**: Cohesion & tokens / Missed opportunities
- **Estimated scope**: 1 file, about 12 HTML/JavaScript lines

## Problem

The three services already use a group reveal, but their 120ms stagger exceeds the audit's 30–80ms decorative range:

```js
/* index.html:1228-1234 — current */
gsap.utils.toArray('.reveal-stagger').forEach(group => {
  gsap.to(group.children, {
    opacity: 1, y: 0, duration: 1, ease: 'expo.out', stagger: 0.12,
    scrollTrigger: { trigger: group, start: 'top 80%' }
  });
});
```

The four same-row statistics are independent `.reveal-up` elements:

```html
<!-- index.html:1046-1047 — exact current opening tags -->
<div class="stats">
  <div class="stat reveal-up">

<!-- index.html:1051, 1055, and 1059 repeat this exact opening tag -->
<div class="stat reveal-up">
```

Because all four have the same top coordinate and threshold, they enter simultaneously instead of reading as a group.

## Target

Use one exact stagger inside the audit's 30–80ms range: **60ms** (`0.06` seconds). It is decorative only and must not delay interaction.

Apply these exact class changes while preserving every descendant and closing tag:

```html
<!-- target opening tags -->
<div class="stats reveal-stagger">
  <div class="stat">

<!-- use this exact opening tag for all four cards -->
<div class="stat">
```

After Plan 002 wraps the reveal logic in a reduced-motion branch, update the no-preference group tween to:

```js
/* target inside the !reduceMotion branch */
gsap.utils.toArray('.reveal-stagger').forEach(group => {
  gsap.to(group.children, {
    opacity: 1,
    y: 0,
    duration: 1,
    ease: 'expo.out',
    stagger: 0.06,
    scrollTrigger: { trigger: group, start: 'top 80%' }
  });
});
```

The existing reduced-motion path must continue setting every `.reveal-stagger > *` to full opacity and zero movement immediately.

## Repo conventions to follow

- Reuse the existing `.reveal-stagger` utility rather than creating a second reveal system.
- Keep the existing 20px starting offset and `expo.out` marketing reveal for no-preference users.
- Use exactly 60ms, which lies inside the audit's 30–80ms range.

## Steps

1. Execute Plan 002 first so the reveal code already has explicit reduced/no-preference branches.
2. Add `reveal-stagger` to the `.stats` container.
3. Remove `reveal-up` from each of the four direct `.stat` children; do not change any nested content or `data-count` attributes.
4. Change the shared group `stagger` from `0.12` to exactly `0.06`. This updates both services and statistics.
5. Confirm the statistics counter logic still targets `.stat` independently and still runs once per statistic for no-preference users.
6. Confirm the reduced-motion selector `.reveal-stagger > *` still makes all cards immediately visible.

## Boundaries

- Requires Plan 002.
- Do NOT change the one-second marketing reveal duration, starting Y offset, counter duration, counter values, grid layout, or card copy.
- Do NOT stagger counter completion separately from card entry.
- Do NOT add interaction delays or disable pointer events during the stagger.
- If Plan 002's target reveal branch is absent, STOP and execute that prerequisite instead of recreating it differently.

## Verification

- **Mechanical**: run `git diff --check`. Run `rg -n "stagger: 0\\.12|class=\"stat reveal-up\"" index.html`; it must return no matches. Run `rg -n "stats reveal-stagger|stagger: 0\\.06" index.html`; both must match.
- **Feel check**: serve with `python3 -m http.server 4173` and reload above the services section.
  - At normal speed, services and stats should read left-to-right without feeling serialized.
  - At 10% playback speed, each sibling must start exactly 60ms after the previous one.
  - Cards must remain clickable/selectable throughout; the stagger must not block interaction.
  - With reduced motion enabled, all cards must appear together and stationary.
- **Done when**: both grouped sections use a 60ms decorative stagger for no-preference users and no staggered movement under reduced motion.

# Sprint Plan: Landing Page Implementation

> **Author**: Product Manager
> **Date**: 2026-06-28
> **Status**: Approved — execute in order
> **Scope**: All frontend code in `frontend/web/`

---

## Policy

**No commits to `main` until I (the PM) and the CEO have reviewed and signed off on each sprint.** Each sprint ends with a demo to the CEO. Only after verbal sign-off do you commit and push.

---

## Current State (Before Any Work)

| File | Status |
|------|--------|
| `app/globals.css` | Default Tailwind v4 + daisyUI plugin, no custom theme, has dark/light media queries |
| `app/layout.tsx` | Uses Geist fonts (next/font/google), no Clerk, no `data-theme` |
| `app/page.tsx` | Bare-bones: "Welcome to UpdateApply" + link to `/dashboard` |
| `app/dashboard/page.tsx` | Empty placeholder: renders "Dashboard" |
| `package.json` | Has next, react, daisyUI, tailwindcss v4 — **no Clerk, no @fontsource packages** |
| `tsconfig.json` | Has `@/*` path alias ✅ |
| `next.config.ts` | Empty — no changes needed |
| `postcss.config.mjs` | Tailwind v4 PostCSS — no changes needed |
| `public/` | Empty |
| `components/` | Does not exist |
| `lib/` | Does not exist |

---

## Sprint 0 — Foundations & Tooling

**Goal**: Install dependencies, set up path aliases, create directory scaffold. Nothing visible yet — pure prep.

### Tasks

1. Install font packages:
   ```bash
   pnpm add @fontsource/inter @fontsource/dm-serif-display
   ```
2. Create directory structure:
   - `components/layout/`
   - `components/landing/`
   - `components/shared/`
   - `lib/api/`
3. Verify `@/*` path alias in `tsconfig.json` (already exists ✅)
4. Verify `next.config.ts` and `postcss.config.mjs` need no changes

### What to Ask CEO

**Nothing.** This is mechanical setup.

### Component Decision

No UI components. Pure dependency installation and scaffolding.

### Commit Gate

CEO does not need to review this sprint — it has no visible output. Devs may commit after setup is verified working (`pnpm dev` starts without errors).

---

## Sprint 1 — Theme Foundation + Layout Shell

**Goal**: The branded chrome that wraps every page. CEO should see the navy/amber/off-white palette, the serif headings, and the nav/footer structure.

### Files to Create/Modify

| File | Action |
|------|--------|
| `app/globals.css` | **Replace** — add custom `update-apply` daisyUI theme, `@theme inline` for font tokens |
| `app/layout.tsx` | **Replace** — import Inter & DM Serif Display, add `data-theme="update-apply"`, set body classes (`bg-base-200`, `text-base-content`, `font-sans`) |
| `components/layout/header.tsx` | **Create** — daisyUI `navbar` with brand logo, nav links, Sign In / Get Started buttons |
| `components/layout/footer.tsx` | **Create** — daisyUI `footer` with Product/Support/Legal link columns + copyright |

### What to Ask CEO

1. **Logo SVG** — The brand mark that goes in the header next to "UpdateApply" text. Without this, devs will use plain text only (`font-heading text-xl text-primary`). Is that acceptable for now, or do you have an SVG?
2. **Header link pages** — Spec lists Home and Dashboard. Do you want any other nav links visible pre-auth? (Features? Pricing? About?)
3. **Footer link target pages** — Features, Pricing, Contact, FAQ, Privacy Policy, Terms of Service — should these link to real pages or just use `href="#"` placeholders for now?

### Component Decision

**daisyUI `navbar` and `footer`** cover this completely. **No shadcn needed.**

### Verification (Show CEO)

- [ ] `<html>` has `data-theme="update-apply"`
- [ ] Body background is `#F8F6F3` (warm off-white)
- [ ] Heading text renders in DM Serif Display (serif)
- [ ] Body text renders in Inter (sans-serif)
- [ ] Header shows at top with logo + nav links
- [ ] Footer shows at bottom with 3 link columns
- [ ] Mobile: hamburger menu appears below 1024px

### Commit

Only after CEO signs off on the look and feel.

---

## Sprint 2 — API Client Layer

**Goal**: The data plumbing that all interactive features will use. Can run in parallel with Sprint 1.

### Files to Create

| File | Action |
|------|--------|
| `lib/api/client.ts` | **Create** — base fetch wrapper with JWT injection, error typing |
| `lib/api/user.ts` | **Create** — `createUser()`, `getUser()`, `updateProfile()` |
| `lib/api/jobs.ts` | **Create** — `getMatches()`, `getJobDetail()`, `generateResume()` |

### What to Ask CEO

1. **Backend API base URL** — The spec defaults to `http://localhost:8000`. What will the production/staging URL be? Should devs add a `NEXT_PUBLIC_API_URL` env var with a fallback?
2. **Auth token flow** — Does the backend expect Clerk JWTs in the `Authorization: Bearer <token>` header, or a custom header? Confirm before wiring `getToken()`.

### Component Decision

Pure TypeScript, no UI components. **No shadcn or daisyUI needed.**

### Verification (Dev-Internal, No CEO Demo Needed)

- [ ] `apiClient.get<T>()` compiles with strict TypeScript
- [ ] Error responses are caught and typed as `ApiError`
- [ ] No `fetch` calls will be scattered in components — all go through client

### Commit

After Sprint 1 is verified working and signed off. Can commit alongside Sprint 1 since they're independent.

---

## Sprint 3 — Landing Page: Hero + How It Works (Top of Fold)

**Goal**: The first thing visitors see. CEO should see the headline, subheadline, primary CTA, provider badges, and the 3-step process section.

### Files to Create/Modify

| File | Action |
|------|--------|
| `components/landing/hero.tsx` | **Create** — daisyUI `hero` layout, headline, subheadline, CTA, provider badges |
| `components/landing/how-it-works.tsx` | **Create** — 3-step Connect → Extract → Apply with numbered circles |
| `app/page.tsx` | **Replace** — compose Header + Hero + HowItWorks + Footer (partial assembly) |

### What to Ask CEO

1. **Hero illustration/visual** — Spec uses a gradient circle (`w-72 h-72 rounded-full bg-gradient-to-br from-primary/10 via-accent/10 to-secondary/10`) as a placeholder. Do you want a real illustration here? If so, provide an SVG or Lottie file. If not, the gradient placeholder is fine for MVP.
2. **Provider badge icons** — The spec lists GitHub, Google Drive, Notion as text badges (`badge badge-outline`). Do you have SVG icons for these, or should devs leave them as text-only badges? **Critical: icons cannot be emoji (PM Plan §7.1).**
3. **Headline copy approval** — "Stop rewriting your resume for every job." Is this final, or do you want alternatives?
4. **Step illustration** — For the 3-step numbers (01, 02, 03), devs are using numbered circles. Do you want line-art SVGs for each step instead, or are numbered circles acceptable?

### Component Decision

**daisyUI `hero`, `hero-content`, `badge`, `btn`** cover everything. **No shadcn needed.** All components are Server Components — zero client JS.

### Verification (Show CEO)

- [ ] Hero renders full-viewport height with headline + CTA
- [ ] "Get Started Free" button is navy (`bg-primary`) with white text
- [ ] Provider badges (GitHub, Google Drive, Notion) render below CTA
- [ ] "How It Works" section has 3 numbered steps with connector line
- [ ] Page works at 320px, 768px, 1440px — no broken layout
- [ ] No emoji anywhere
- [ ] No horizontal scroll
- [ ] Touch targets ≥44×44px on mobile

### Commit

Only after CEO approves the hero and steps visually.

---

## Sprint 4 — Landing Page: Features + Providers + CTA Section + Full Assembly

**Goal**: The complete landing page. CEO should see all 5 sections in order: Hero → How It Works → Features → Providers → CTA → Footer.

### Files to Create/Modify

| File | Action |
|------|--------|
| `components/landing/features.tsx` | **Create** — 6 benefit cards in a responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`) |
| `components/landing/providers.tsx` | **Create** — Platform cards with initial-letter placeholder icons |
| `components/landing/cta-section.tsx` | **Create** — Navy background section with amber CTA button |
| `app/page.tsx` | **Update** — Add Features, Providers, CtaSection imports and render them |

### What to Ask CEO

1. **Feature card icons** — Each of the 6 feature cards has a placeholder circle with an initial letter. Do you have line-art SVGs for: Zero Data Entry, One-Click Matching, Perfect Fit, Always Synced, Smarter Over Time, Privacy First? If not, devs will leave the initial-letter placeholders. (Per PM Plan §7.3, SVG icon components must accept a `className` prop.)
2. **Provider icon SVGs** — Re-ask from Sprint 3 if not provided yet. The providers section needs GitHub, Google Drive, Notion logos. Text-only badges were used in Sprint 3; this section needs proper cards with icons.
3. **CTA copy** — "Ready to stop rewriting?" + "Get Started Free" button. Is this final?
4. **Lottie animations** — The spec mentions Lottie as a possibility for feature illustrations. Do you have Lottie JSON files, or should devs skip animations entirely for MVP?

### Component Decision

**daisyUI `card`, `card-body`, `card-title`, `btn`, `grid`** classes cover everything. **No shadcn needed.** All are Server Components.

### Verification (Show CEO Complete Page)

- [ ] All 5 sections render in correct order: Hero → How It Works → Features → Providers → CTA → Footer
- [ ] Features grid: 6 cards, 3 columns on desktop, 2 on tablet, 1 on mobile
- [ ] Provider cards show 3 platforms with placeholder icons
- [ ] CTA section has navy background with amber button
- [ ] Page is fully responsive: 320px, 768px, 1440px
- [ ] Heading hierarchy: 1 `<h1>` (hero headline), multiple `<h2>` (section titles), `<h3>` (card titles)
- [ ] Semantic HTML: `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>` all correct
- [ ] No `"use client"` on any component
- [ ] No emoji anywhere
- [ ] Lighthouse Performance ≥ 90
- [ ] Total JS bundle < 200 KB gzipped

### Commit

Only after CEO walks through the full page and signs off.

---

## Sprint 5 — Authentication (Clerk)

**Goal**: "Get Started Free" and "Sign In" buttons actually work. CEO should be able to click through to a sign-up flow and land on the dashboard.

### Files to Create/Modify

| File | Action |
|------|--------|
| `.env.local` | **Create** — Clerk keys + API URL (gitignored) |
| `middleware.ts` | **Create** — Clerk middleware protecting `/dashboard/*`, `/resume/*` |
| `app/layout.tsx` | **Update** — Wrap with `<ClerkProvider>` |
| `components/layout/auth-section.tsx` | **Create** — Client component with Clerk buttons + UserButton |
| `components/layout/header.tsx` | **Update** — Replace static buttons with `<AuthSection />` |

### What to Ask CEO

1. **Clerk API keys** — Go to [dashboard.clerk.com](https://dashboard.clerk.com), create an application, and provide:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` (starts with `pk_test_` or `pk_live_`)
   - `CLERK_SECRET_KEY` (starts with `sk_test_` or `sk_live_`)
2. **Sign-in flow preference** — Option A: **Modal overlay** (Sign In / Sign Up opens as a popup modal, no page redirect — cleaner UX). Option B: **Dedicated `/sign-in` and `/sign-up` pages** (traditional route-based auth).
3. **Post-sign-up redirect** — Where should users land after first sign-up? Option A: `/onboarding` (setup wizard). Option B: `/dashboard` (straight to matches).
4. **Social login providers** — Clerk supports Google, GitHub, etc. Do you want social login buttons, or email/password only?
5. **shadcn Dialog vs daisyUI modal** — If you choose modal flow, daisyUI `modal` (native `<dialog>`) works well. If you want a more complex controlled dialog with focus trapping, devs would install shadcn `Dialog` instead. **Recommendation**: daisyUI `modal` is sufficient for this use case.

### Component Decision

`AuthSection` must be `"use client"` (needs `useAuth()` hook). **daisyUI `btn`** classes used for the buttons. **shadcn Dialog is optional** — only if CEO prefers a specific modal behavior that daisyUI's native dialog can't achieve.

### Verification (Show CEO)

- [ ] Landing page is public — no auth required to view
- [ ] Clicking "Get Started Free" opens sign-up flow
- [ ] Clicking "Sign In" opens sign-in flow
- [ ] After sign-in, `/dashboard` loads (even if empty)
- [ ] Unauthenticated users trying to visit `/dashboard` are redirected to sign-in
- [ ] Header shows UserButton (avatar) when signed in
- [ ] No Clerk tokens in localStorage or sessionStorage

### Commit

Only after CEO creates a test account successfully and confirms the flow.

---

## Sprint 6 — Final Polish, Responsive QA & Performance

**Goal**: Production-ready quality. CEO should see a pixel-perfect, fast, accessible page.

### Tasks

1. Run Lighthouse on landing page — target ≥ 90 Performance, ≥ 90 Accessibility
2. Test all 3 breakpoints: 320px, 768px, 1440px — fix any issues
3. Keyboard navigation audit — Tab through every interactive element
4. Screen reader audit — headings, landmarks, alt text
5. Check bundle size — `next build` should show landing page JS < 200 KB gzipped
6. Verify `prefers-reduced-motion` is respected (daisyUI does this by default)
7. Final CEO walkthrough

### What to Ask CEO

Nothing new. This is pure QA.

### Verification (Final Sign-Off)

- [ ] Lighthouse Performance ≥ 90
- [ ] Lighthouse Accessibility ≥ 90
- [ ] All breakpoints render without issues
- [ ] Keyboard navigation works end-to-end
- [ ] Screen reader announces all content in logical order
- [ ] No emoji, no `dangerouslySetInnerHTML`, no inline styles
- [ ] CEO has walked through the full page and approves

### Commit

Final commit after CEO signs off. **This is the commit that goes to `main`.**

---

## Summary Timeline

```
Sprint 0 (Tooling)         ──────────┤ (commit, no review needed)
                                       │
Sprint 1 (Theme + Shell)   ──────────┤ (parallel with Sprint 2)
                                       │
Sprint 2 (API Client)      ──────────┤ (parallel with Sprint 1)
                                       │
                                       ├── CEO reviews Sprint 1 + 2 ──► commit
                                       │
Sprint 3 (Hero + Steps)    ──────────┤ 
                                       ├── CEO reviews Sprint 3 ──► commit
                                       │
Sprint 4 (Full Landing)    ──────────┤
                                       ├── CEO reviews Sprint 4 ──► commit
                                       │
Sprint 5 (Auth)            ──────────┤
                                       ├── CEO reviews Sprint 5 ──► commit
                                       │
Sprint 6 (QA + Polish)     ──────────┤
                                       └── CEO final sign-off ──► commit to main
```

Each sprint builds on the previous one. **No sprint is marked done until the CEO says "ship it."**

---

## Things the CEO Needs to Decide / Provide

Consolidated list of everything the dev team needs from the CEO, organized by urgency:

### 🟢 Before Sprint 1 (Now)

- [ ] **Logo SVG** — or confirm text-only brand mark is acceptable for now
- [ ] **Header nav links** — just "Home" + "Dashboard", or more?
- [ ] **Footer link targets** — placeholder `#` or real pages?

### 🟡 Before Sprint 3 (Soon)

- [ ] **Provider badge icons** — GitHub, Google Drive, Notion SVGs, or text badges?
- [ ] **Hero illustration** — real artwork or keep gradient placeholder?
- [ ] **Headline copy** — "Stop rewriting your resume for every job." Final?
- [ ] **Step illustrations** — numbered circles OK, or need SVGs?

### 🟠 Before Sprint 4 (Mid)

- [ ] **Feature card SVGs** — 6 line-art icons for the benefit cards?
- [ ] **Lottie animations** — any, or skip for MVP?

### 🔴 Before Sprint 5 (Late)

- [ ] **Clerk API keys** — from Clerk Dashboard
- [ ] **Sign-in flow** — modal overlay vs. dedicated pages?
- [ ] **Post-sign-up redirect** — `/onboarding` or `/dashboard`?
- [ ] **Social login** — Google/GitHub OAuth, or email only?

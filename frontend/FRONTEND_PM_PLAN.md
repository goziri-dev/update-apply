# UpdateApply Frontend — Product Manager Design Plan

> **Author**: Product Manager  
> **Status**: Living document — updated as decisions are made  
> **Scope**: All frontend code in `frontend/web/`

---

## Role & Authority

This document defines the design principles, technical constraints, component selection hierarchy, code organization rules, and quality gates that govern **all** frontend work. Every developer, designer, or reviewer must refer to this document before writing or reviewing any code. Deviations require explicit PM sign-off.

---

## Table of Contents

1. [Tech Stack & Tooling](#1-tech-stack--tooling)
2. [Component Selection Hierarchy](#2-component-selection-hierarchy)
3. [Responsive Design Mandate](#3-responsive-design-mandate)
4. [Code Organization Rules](#4-code-organization-rules)
5. [Security & Privacy Constraints](#5-security--privacy-constraints)
6. [Accessibility Standards](#6-accessibility-standards)
7. [Icon & Asset Policy](#7-icon--asset-policy)
8. [Performance Budget](#8-performance-budget)
9. [Page Architecture & User Journey](#9-page-architecture--user-journey)
10. [Component Inventory & Selection Guide](#10-component-inventory--selection-guide)
11. [State Management Strategy](#11-state-management-strategy)
12. [API Integration Patterns](#12-api-integration-patterns)
13. [Quality Gates — Review Checklist](#13-quality-gates--review-checklist)
14. [Implementation Phases](#14-implementation-phases)
15. [Open Questions & Decisions Log](#15-open-questions--decisions-log)

---

## 1. Tech Stack & Tooling

| Layer | Choice | Notes |
|-------|--------|-------|
| Framework | Next.js 16 (App Router) | Server Components by default; `"use client"` only when interactivity required |
| Language | TypeScript 5 | Strict mode enabled |
| Styling | Tailwind CSS 4 + daisyUI 5 | CSS `@import "tailwindcss"` + `@plugin "daisyui"` |
| Component Library (Primary) | **daisyUI 5** | For layout, navigation, forms, alerts, cards, and all standard UI |
| Component Library (Secondary) | **shadcn/ui** (via MCP) | For complex interactive widgets that daisyUI doesn't cover well |
| Fallback | Tailwind CSS 4 utilities | Only when neither daisyUI nor shadcn provides what's needed |
| Icons | User-provided SVGs / Lottie files | No emoji, no icon font libraries. See §7. |
| Auth | Clerk (`@clerk/nextjs`) | Frontend-managed auth; JWT tokens forwarded to backend |
| Package Manager | pnpm | Already configured |

### What is already installed

- `daisyui@^5.5.23` + `@tailwindcss/postcss@^4` — ready in `globals.css`
- `next@16.2.9`, `react@19.2.4`, `typescript@5` with strict mode
- shadcn MCP server configured in `.vscode/mcp.json`

### What needs to be installed

- `@clerk/nextjs` — for authentication integration
- shadcn components — install on-demand via `pnpm dlx shadcn@latest add <component>` via the MCP server

---

## 2. Component Selection Hierarchy

**This hierarchy is absolute. Do not deviate.**

```
┌─────────────────────────────────────────────┐
│  1. daisyUI 5 (first choice)                │
│     For: buttons, cards, navbars, forms,    │
│     alerts, modals, steps, tabs, tables,    │
│     loading states, pagination, etc.        │
│     → Add daisyUI class names to HTML       │
│     → Customize ONLY with daisyUI color      │
│       classes or Tailwind utility classes    │
│     → If a daisyUI component class exists,   │
│       you MUST use it                       │
└─────────────────────┬───────────────────────┘
                      │ falls back to
                      ▼
┌─────────────────────────────────────────────┐
│  2. shadcn/ui (via MCP)                     │
│     For: complex interactive widgets—       │
│     dialogs, advanced forms, dropdowns,     │
│     date pickers, multi-select, etc.        │
│     → Only use if daisyUI doesn't have      │
│       a suitable component or the daisyUI   │
│       version is insufficiently interactive │
│     → Install via: pnpm dlx shadcn@latest   │
│       add <component>                       │
│     → Generated files go to                 │
│       components/ui/                        │
└─────────────────────┬───────────────────────┘
                      │ falls back to
                      ▼
┌─────────────────────────────────────────────┐
│  3. Tailwind CSS 4 utilities + semantic HTML│
│     For: custom layouts, bespoke sections   │
│     that no component library provides      │
│     → Use semantic HTML tags (<header>,     │
│       <section>, <article>, <nav>, etc.)    │
│     → Keep custom CSS to absolute minimum   │
│     → Prefer Tailwind utility classes       │
└─────────────────────────────────────────────┘
```

### Decision Rules

When implementing any UI element:

1. **Search daisyUI's component list** (from `llms.txt` or daisyUI docs) for a match. If found → use it.
2. If daisyUI's component doesn't meet the interaction requirements (e.g., complex multi-step dialog, advanced form validation) → check shadcn.
3. If neither covers the need → build with semantic HTML + Tailwind utilities.
4. **Never import both a daisyUI component AND a shadcn component that serve the same purpose** (e.g., don't use daisyUI `modal` AND shadcn `Dialog` in the same project — pick one and be consistent).

### daisyUI 5 Component Reference (Quick Catalog)

| Category | Available Components |
|----------|---------------------|
| **Layout** | `hero`, `navbar`, `footer`, `drawer`, `stack`, `divider` |
| **Navigation** | `menu`, `breadcrumbs`, `tabs`, `steps`, `pagination`, `dock`, `megamenu` |
| **Content** | `card`, `carousel`, `collapse`, `accordion`, `list`, `stat`, `timeline` |
| **Forms** | `input`, `textarea`, `select`, `checkbox`, `radio`, `toggle`, `range`, `file-input`, `label`, `fieldset`, `validator`, `otp` |
| **Feedback** | `alert`, `loading`, `progress`, `radial-progress`, `skeleton`, `toast`, `tooltip` |
| **Actions** | `btn`, `dropdown`, `modal`, `swap`, `fab` |
| **Data Display** | `badge`, `avatar`, `avatar-group`, `table`, `kbd`, `status`, `countdown` |
| **Visual** | `aura`, `mask`, `diff`, `hover-3d`, `hover-gallery`, `text-rotate`, `mockup-*` |
| **Theme** | `theme-controller` |

### shadcn Components to Prefer (when daisyUI insufficient)

| shadcn Component | Use When |
|-----------------|----------|
| `Dialog` | Controlled open/close + focus trap needed (daisyUI `modal` for simple cases) |
| `Sheet` | Slide-in panels (daisyUI `drawer` for sidebar) |
| `Form` + React Hook Form | Complex multi-field forms with validation |
| `Toast` | If daisyUI `toast` styling is insufficient for the use case |
| `Command` / `Popover` | Searchable dropdowns, command palettes |
| `Skeleton` | If daisyUI `skeleton` is insufficient for complex loading states |

---

## 3. Responsive Design Mandate

**Every view, every component, every page MUST be fully responsive on:**
- Mobile: 320px–767px
- Tablet: 768px–1023px
- Desktop: 1024px+

### Rules

1. **Mobile-first CSS**: Write base styles for mobile, then `sm:`, `md:`, `lg:` breakpoints to enhance for larger screens.
2. **No horizontal scroll** on any viewport width. Use `overflow-x-auto` only for data tables.
3. **Touch targets** must be at least 44×44px on mobile (buttons, links, form controls).
4. **Navigation** on mobile must use either:
   - daisyUI `drawer` with `lg:drawer-open` (sidebar pattern)
   - daisyUI `dropdown` / `dock` (bottom-nav pattern)
   - A hamburger menu (via daisyUI `drawer-toggle`)
5. **Typography**: Use responsive text sizes (`text-sm md:text-base lg:text-lg` pattern). Never use fixed px.
6. **Grids**: Use Tailwind's responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`). Never fixed-width columns.
7. **Test** every component at 320px, 768px, and 1440px widths before marking complete.
8. **Images**: Use `max-w-full h-auto` on all images. Provide `sizes` attribute on `<img>` for responsive loading.

---

## 4. Code Organization Rules

### 4.1 File Structure

```
frontend/web/
├── app/
│   ├── layout.tsx              ← Root layout (ClerkProvider, fonts, theme)
│   ├── page.tsx                ← Landing page (imports section components)
│   ├── globals.css             ← Tailwind + daisyUI + custom theme
│   ├── dashboard/
│   │   ├── page.tsx            ← Dashboard main page
│   │   ├── matches/
│   │   │   └── page.tsx        ← Job matches list
│   │   └── profile/
│   │       └── page.tsx        ← Profile/onboarding
│   ├── resume/
│   │   └── [id]/
│   │       └── page.tsx        ← Resume view/download
│   └── (auth)/
│       └── callback/
│           └── page.tsx        ← OAuth callback handler
│
├── components/
│   ├── landing/                ← Landing page sections only
│   │   ├── hero.tsx
│   │   ├── how-it-works.tsx
│   │   ├── features.tsx
│   │   ├── providers.tsx
│   │   └── cta-section.tsx
│   ├── layout/                 ← Shared layout components
│   │   ├── header.tsx          ← Navbar
│   │   └── footer.tsx          ← Footer
│   ├── ui/                     ← shadcn-generated components
│   │   ├── button.tsx          ← (shadcn — via MCP)
│   │   ├── dialog.tsx          ← (shadcn — via MCP)
│   │   └── ...                 ← (other shadcn components)
│   ├── providers/              ← Provider-specific UI
│   │   ├── github-icon.tsx
│   │   ├── google-drive-icon.tsx
│   │   └── notion-icon.tsx
│   └── shared/                 ← Reusable shared components
│       ├── job-card.tsx         ← Used in multiple pages
│       └── profile-form.tsx     ← Used in onboarding + settings
│
├── lib/                        ← Non-component code
│   ├── api/                    ← API client layer
│   │   ├── client.ts           ← Base fetch wrapper
│   │   ├── user.ts             ← User endpoints
│   │   └── jobs.ts             ← Job endpoints
│   └── utils.ts                ← Shared utility functions
│
└── public/
    ├── icons/                  ← Downloaded SVG/Lottie icons
    └── images/                 ← Static images
```

### 4.2 One Concern Per File Rule

**Every file MUST contain exactly one exported component or one module concern.**

- ✅ `hero.tsx` — exports only `Hero` component
- ✅ `api/client.ts` — exports only the API client
- ❌ `hero.tsx` — exports `Hero` AND `HeroSubtitle` helper (unless it's a tiny private helper <20 lines used only there)
- ❌ A page file that also defines components inline (extract to `components/`)

### 4.3 No Duplication Rule

Before creating any new component or utility, search the codebase for existing implementations. Flag and eliminate duplication.

**Checklist to run before adding any code:**
1. Does a daisyUI class already do this? → Use the class.
2. Does a shadcn component already do this? → Import it.
3. Does a component in `components/shared/` already do this? → Reuse/extend it.
4. Does a utility in `lib/` already do this? → Import it.

**Penalty violations (will be blocked in review):**
- Two different card component implementations with identical layout logic
- Two different API call patterns (one using `fetch`, another using a different wrapper)
- Inline styles when a daisyUI class or Tailwind utility exists

---

## 5. Security & Privacy Constraints

### 5.1 Authentication (Clerk)

- Wrap the root `layout.tsx` with `<ClerkProvider>`.
- Protect routes via `clerkMiddleware` in `middleware.ts`.
- Never store Clerk session tokens in `localStorage` or `sessionStorage` — Clerk manages this internally.
- Add `clerkMiddleware` to protect `/dashboard/*` and `/resume/*` routes.
- Landing page (`/`) is public; the "Get Started Free" CTA opens `<SignUpButton />`.

### 5.2 API Calls to Backend

- All API calls go through a centralized client in `lib/api/client.ts`.
- The client attaches the Clerk JWT to the `Authorization` header via `useAuth()` or `getToken()`.
- Never send raw user input directly to the backend without validation.
- Use Zod or React Hook Form resolvers for client-side validation before sending.

### 5.3 XSS & Injection Prevention

- Use React/Next.js's built-in escaping. Never use `dangerouslySetInnerHTML`.
- If HTML rendering is needed for resume previews, sanitize with DOMPurify or equivalent.
- Never interpolate user input into `<style>` tags or `href="javascript:..."`.

### 5.4 Environment & Secrets

- All environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Never put secrets here.
- Backend API keys, Clerk secret keys, and database URLs go in `.env.local` (gitignored).

---

## 6. Accessibility Standards

| Requirement | Standard |
|-------------|----------|
| **Semantic HTML** | Use `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>` appropriately |
| **Heading hierarchy** | One `<h1>` per page. No skipping levels (h1→h2→h3, never h1→h3) |
| **Form labels** | Every `<input>`, `<select>`, `<textarea>` must have an associated `<label>` or `aria-label` |
| **Focus management** | Visible focus indicators on all interactive elements (daisyUI provides this by default) |
| **Keyboard navigation** | All interactive elements must be reachable and operable via keyboard alone |
| **ARIA** | Add `role`, `aria-label`, `aria-describedby` where semantic HTML is insufficient |
| **Color contrast** | Meet WCAG AA minimum (4.5:1 for normal text, 3:1 for large text). daisyUI themes respect this by default |
| **Reduced motion** | Respect `prefers-reduced-motion`. daisyUI 5.6 supports this for loading animations |
| **Screen readers** | Use `sr-only` for screen-reader-only text. Add `aria-live="polite"` for dynamic content |

---

## 7. Icon & Asset Policy

### 7.1 No Emoji in UI

- **Emojis are strictly forbidden** in the user-facing interface.
- Not in buttons, not in cards, not in headers, not in empty states, not in error messages.
- Exception: In internal comments, documentation, or commit messages only.

### 7.2 Icon Sources

All icons will be **user-provided** (downloaded and placed in `public/icons/`):

| Icon Needed | Format | Location |
|-------------|--------|----------|
| UpdateApply logo | SVG | `public/icons/logo.svg` |
| GitHub logo | SVG | `public/icons/github.svg` |
| Google Drive logo | SVG | `public/icons/google-drive.svg` |
| Notion logo | SVG | `public/icons/notion.svg` |
| Feature/benefit illustrations | Lottie JSON or SVG | `public/icons/feature-*.svg` |
| Social links | SVG | `public/icons/*.svg` |
| Navigation / utility | SVG | `public/icons/*.svg` |

### 7.3 Icon Components

- For SVG icons: Create a React component per icon in `components/providers/` that wraps the SVG inline (not as an `<img>` tag), so colors can inherit from CSS.
- For Lottie animations: Use `lottie-react` or `@dotlottie/react-player` to load JSON files from `public/icons/`.
- Each icon component must accept `className` for size/color overrides.

---

## 8. Performance Budget

| Metric | Target |
|--------|--------|
| **Lighthouse Performance** | ≥ 90 on mobile and desktop |
| **First Contentful Paint (FCP)** | < 1.5s |
| **Largest Contentful Paint (LCP)** | < 2.5s |
| **Total JS bundle** | < 200 KB (gzipped) for landing page |
| **CLS** | < 0.1 |
| **Images** | All images must have `width` and `height` attributes or `aspect-ratio` to prevent layout shift |

### Performance Rules

1. **Prefer Server Components**: Only add `"use client"` when you need browser APIs, event handlers, or state.
2. **Lazy load** below-the-fold content on the landing page using dynamic imports.
3. **No large libraries** on the landing page. Defer chart libraries, PDF generators, and heavy form libraries to feature pages.
4. **Use Next.js `<Image>`** (not `<img>`) for all static images in `public/`.
5. **Bundle analysis**: Run `next build` and check the `.next/analyze` output before shipping.

---

## 9. Page Architecture & User Journey

### 9.1 User Flow Map

```
                    ┌──────────────┐
                    │  Landing     │  Public
                    │  Page (/)    │
                    └──────┬───────┘
                           │ "Get Started Free"
                           ▼
                    ┌──────────────┐
                    │  Sign Up /   │  Clerk Modal
                    │  Sign In     │  (overlay, no redirect)
                    └──────┬───────┘
                           │ First time?
                           ▼
                    ┌──────────────┐
                    │  Onboarding  │  Multi-step wizard
                    │  Wizard      │  (if first login)
                    │              │
                    │ Step 1:      │
                    │   Connect    │
                    │   Providers  │
                    │ Step 2:      │
                    │   Build      │
                    │   Profile    │
                    │ Step 3:      │
                    │   First Sync │
                    └──────┬───────┘
                           │ Complete or Skip
                           ▼
                    ┌──────────────┐
                    │  Dashboard   │  Protected
                    │  (/dashboard)│
                    │              │
                    │  ├─ Job      │
                    │  │  Matches  │
                    │  ├─ Profile  │
                    │  │  Summary  │
                    │  └─ Sync    │
                    │     Status  │
                    └──────┬───────┘
                           │ Select match
                           ▼
                    ┌──────────────┐
                    │  Resume      │  Protected
                    │  Generation  │
                    │  (/resume/   │
                    │    [id])     │
                    └──────────────┘
```

### 9.2 Page-by-Page Requirements

#### Landing Page (`/`) — PUBLIC

| Section | Component | daisyUI Classes | Notes |
|---------|-----------|-----------------|-------|
| Top nav | `Header` | `navbar`, `navbar-start/center/end` | Logo left; "Sign In" + "Get Started" right |
| Hero | `Hero` | `hero`, `hero-content` | Headline, subheadline, CTA button, provider badges |
| How It Works | `HowItWorks` | `steps` or custom grid with `card` | 3-step visual flow |
| Features | `Features` | `card` grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`) | 6 feature cards |
| Providers | `Providers` | `card` with logos | GitHub, Google Drive, Notion |
| CTA Section | `CtaSection` | `hero` or `card` with `bg-primary` | Final conversion push |
| Footer | `Footer` | `footer`, `footer-center`, `lg:footer-horizontal` | Links, social, copyright |

#### Dashboard (`/dashboard`) — PROTECTED

| Section | Notes |
|---------|-------|
| Sidebar | daisyUI `drawer` with `lg:drawer-open`; contains user avatar, nav links |
| Main content | Match cards, profile completeness indicator, quick-action buttons |
| Job matches | Grid of daisyUI `card` components showing match score, company, title |

#### Onboarding Wizard — PROTECTED

Multi-step form using daisyUI `steps` component for progress indication:
- **Step 1**: Provider connection (GitHub, Google Drive, Notion buttons)
- **Step 2**: Profile form (occupation, location, preferences — uses `input`, `select`, `toggle`)
- **Step 3**: Sync trigger (progress via `progress` bar or `loading` spinner)

---

## 10. Component Inventory & Selection Guide

### Landing Page Component Mapping

| UI Element | daisyUI Choice | Why This Choice | Fallback If Missing |
|-----------|----------------|-----------------|-------------------|
| Primary CTA button | `btn btn-primary btn-lg` | daisyUI has comprehensive button system | — |
| Secondary buttons | `btn btn-outline` | Built-in style variant | — |
| Hero layout | `hero` + `hero-content` | Purpose-built for large hero sections | Flexbox layout |
| Navbar | `navbar` + `navbar-start/center/end` | Handles responsive positioning | — |
| Footer | `footer` + `lg:footer-horizontal` | Supports multi-column, responsive | Grid layout |
| Cards (features) | `card` + `card-body` + `card-title` | Rich card system with sizes | shadcn `Card` |
| Steps (how it works) | `steps` + `step` + `step-primary` | Native step indicator | Custom grid |
| Provider logos | Avatar or custom | Simple image display | — |
| Modals | `modal` (dialog element) | Works with HTML `<dialog>`, accessible | shadcn `Dialog` |
| Loading states | `skeleton` + `skeleton-text` | Lightweight, themable | shadcn `Skeleton` |
| Form inputs | `input` + `label` / `floating-label` | Themed, size variants | shadcn `Input` |
| Dropdown menus | `dropdown` (popover API) | Modern, accessible | shadcn `DropdownMenu` |
| Alerts / toasts | `alert` + `toast` | Themed, color variants | shadcn `Toast` |
| Page divider | `divider` | Simple, themed | — |

### Shared Components to Build

| Component | File | Why Shared |
|-----------|------|-----------|
| `JobCard` | `components/shared/job-card.tsx` | Used in dashboard, matches list, possibly landing preview |
| `ProviderButton` | `components/shared/provider-button.tsx` | Used in landing, onboarding, settings |
| `ProfileForm` | `components/shared/profile-form.tsx` | Used in onboarding wizard + profile settings |
| `MatchScore` | `components/shared/match-score.tsx` | Used in job cards and detail views |

### What NOT to Build

| Item | Alternative |
|------|------------|
| Custom button component | Use daisyUI `btn` class directly |
| Custom card wrapper | Use daisyUI `card` class directly |
| Custom form layout | Use daisyUI `fieldset` + `label` |
| Custom theme switcher | Use daisyUI `theme-controller` |

---

## 11. State Management Strategy

### Rules

1. **Server State** (data from backend): Use React Server Components + fetch where possible. For interactive features, use a thin client layer with `fetch` + `useEffect` or SWR/React Query if complexity grows.
2. **Auth State**: Managed entirely by Clerk. Access via `useAuth()` / `useUser()` hooks.
3. **UI State**: Local `useState` or `useReducer` within the component. No global state store unless proven necessary.
4. **Form State**: React Hook Form (via shadcn `Form` component) for complex forms. Native `<form>` with `useState` for simple forms.
5. **No Redux, No Zustand, No Context-for-everything**. If you need to share state between distant components, first ask: "Can I lift state to a Server Component and pass it as props?" If yes, do that. If truly necessary, create a focused Context.

### Data Fetching Pattern

```typescript
// ✅ GOOD: Server Component fetching
// app/dashboard/page.tsx
async function DashboardPage() {
  const user = await apiClient.getUser();  // fetch in server component
  return <DashboardClient initialUser={user} />;
}

// ✅ GOOD: Client component with loading fallback
// components/dashboard/job-matches.tsx
"use client";
function JobMatches() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  // fetch in useEffect, show skeleton while loading
}
```

---

## 12. API Integration Patterns

### 12.1 Base Client

`lib/api/client.ts` — wraps `fetch` with:
- Base URL from environment variable
- Clerk JWT token injection
- JSON content-type header
- Error handling wrapper
- Request/response type generics

### 12.2 Endpoint Modules

Each domain area gets its own file in `lib/api/`:
- `lib/api/user.ts` — `createUser()`, `getUser()`, `updateProfile()`
- `lib/api/jobs.ts` — `getMatches()`, `getJobDetail()`, `generateResume()`

### 12.3 Error Handling

- All API errors are caught at the client layer and transformed into typed errors.
- UI surfaces show user-friendly messages (not raw error objects).
- Use daisyUI `alert` with appropriate color (`alert-error`, `alert-warning`).

---

## 13. Quality Gates — Review Checklist

Every code submission MUST pass this checklist before merge.

### 13.1 General
- [ ] File follows the one-component-per-file rule (§4.2)
- [ ] No duplicated logic — checked existing components/lib first (§4.3)
- [ ] daisyUI was the first choice checked before shadcn or Tailwind fallback (§2)
- [ ] All hardcoded strings in user-facing UI are free of implementation jargon (no "RAG", "LLM", "fuzzy keyword match", "pgvector", etc.)

### 13.2 Responsive
- [ ] Mobile-first breakpoints used (`sm:`, `md:`, `lg:`)
- [ ] Tested at 320px — no horizontal scroll, no broken layout
- [ ] Tested at 768px — layout adapts gracefully
- [ ] Tested at 1440px — layout uses available space
- [ ] Touch targets ≥ 44×44px on mobile

### 13.3 Accessibility
- [ ] Semantic HTML tags used (not `<div>` for everything)
- [ ] Heading hierarchy is correct (h1→h2→h3)
- [ ] All form elements have labels
- [ ] Keyboard navigation works (Tab through all interactive elements)
- [ ] `alt` text on all images
- [ ] No `dangerouslySetInnerHTML`

### 13.4 Assets
- [ ] No emoji anywhere in the UI (§7.1)
- [ ] All icons are SVGs or Lottie files from `public/icons/` — no icon font libraries
- [ ] All images have explicit `width` and `height` or `aspect-ratio`

### 13.5 Security
- [ ] No secrets in client-side code
- [ ] All form inputs validated on client before sending
- [ ] Protected routes have Clerk middleware guard
- [ ] API client attaches auth token

### 13.6 Performance
- [ ] Server Component used wherever possible (no unnecessary `"use client"`)
- [ ] No heavy library imports on the landing page
- [ ] Below-fold content uses lazy loading or dynamic imports

---

## 14. Implementation Phases

### Phase 1: Foundation *(can run in parallel)*
- Install shadcn components via MCP (`button`, `skeleton`, `dialog`)
- Set up Clerk provider in root layout + middleware
- Create `lib/api/client.ts` with base fetch wrapper
- Build shared layout components: `Header` + `Footer`
- Create SVG icon wrapper components

### Phase 2: Landing Page *(depends on Phase 1 header/footer)*
- Build each section as its own component file
  - `hero.tsx` → `components/landing/`
  - `how-it-works.tsx` → `components/landing/`
  - `features.tsx` → `components/landing/`
  - `providers.tsx` → `components/landing/`
  - `cta-section.tsx` → `components/landing/`
- Assemble in `app/page.tsx`
- Verify responsive at all breakpoints
- Performance audit (Lighthouse)

### Phase 3: Authentication & Onboarding *(depends on Phase 1)*
- Wire Clerk sign-up/sign-in to landing page CTAs
- Build onboarding wizard (3-step with `steps` component)
- Profile form with validation
- Provider connection buttons

### Phase 4: Dashboard *(depends on Phase 3)*
- Drawer/sidebar layout
- Job matches grid
- Profile summary card
- Sync status indicator

### Phase 5: Resume Generation *(depends on Phase 4)*
- Resume detail page
- Download button
- Status polling for generation progress

---

## 15. Open Questions & Decisions Log

| # | Question | Status | Recommendation |
|---|----------|--------|---------------|
| 1 | Do we install all shadcn components upfront or on-demand? | **Open** | On-demand via MCP when a component is first needed. Keeps bundle lean. |
| 2 | Should we use SWR/React Query for data fetching? | **Open** | Not yet. Start with Server Components + fetch. Add only if client-side caching complexity justifies it. |
| 3 | Lottie player library: `lottie-react` vs `@dotlottie/react-player`? | **Open** | Awaiting user's Lottie file format. Decide when first Lottie asset is provided. |
| 4 | Dark mode strategy? | **Open** | daisyUI supports `data-theme` attribute. Could add a theme toggle using `theme-controller`. Not in MVP scope unless requested. |
| 5 | Should `aria-current="page"` be added to active nav links? | **Decided** | Yes — quick accessibility win. Add to `Header` and sidebar navigation. |

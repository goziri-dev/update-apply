# Theme Implementation Guide — Developer Execution Plan

> **From**: Product Manager & Design
> **To**: Frontend Developers
> **Status**: Approved — execute in order
> **Scope**: All frontend code in `frontend/web/`

---

## How to Use This Document

This is a **sequential execution plan**. Each phase has a dependency on the previous one. Do not skip phases. Within each phase, steps are listed in the order they should be done. Files listed under each step are the **only files** you need to touch for that step.

Before writing any code, read the full document once. Then start from Phase 1.

---

## Phase 0: Current State (What Exists Today)

Before you begin, this is what's already in `frontend/web/`:

| File | Content | Action Needed |
|------|---------|---------------|
| `app/globals.css` | Tailwind v4 import + daisyUI plugin + default CSS vars | **Replace entirely** with custom theme config |
| `app/layout.tsx` | Root layout with Geist fonts, no daisyUI theme attr | **Add** `data-theme`, swap in new fonts |
| `app/page.tsx` | Bare-bones landing with "Welcome to UpdateApply" | **Replace** with composable landing sections |
| `app/dashboard/page.tsx` | Empty "Dashboard" placeholder | Will be expanded in later phase |
| `package.json` | Next.js 16.2.9, daisyUI 5.5.23, Tailwind CSS 4 | No changes needed |
| `postcss.config.mjs` | Tailwind v4 PostCSS config | No changes needed |
| `next.config.ts` | Empty Next.js config | No changes needed |
| `public/` | Empty | Will need SVG icons placed here |

---

## Phase 1: Theme Foundation

**Goal**: Establish the visual foundation so every subsequent component automatically inherits the correct colors, fonts, and styling.

### Step 1.1 — Configure Custom daisyUI Theme in `globals.css`

**File**: `app/globals.css`

Replace the entire file content with:

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: {
    "update-apply": {
      "color-scheme": "light",
      "primary": "#1E3A5F",
      "primary-content": "#FFFFFF",
      "secondary": "#D4954E",
      "secondary-content": "#1A1A1A",
      "accent": "#5B8C7E",
      "accent-content": "#FFFFFF",
      "neutral": "#E5E0DA",
      "neutral-content": "#2D2A28",
      "base-100": "#FFFFFF",
      "base-200": "#F8F6F3",
      "base-300": "#EDE9E4",
      "base-content": "#2D2A28",
      "info": "#6B9BC4",
      "success": "#5B8C7E",
      "warning": "#D4954E",
      "error": "#C4544A",
    },
  },
}

@theme inline {
  --font-heading: "DM Serif Display", serif;
  --font-sans: "Inter", sans-serif;
}
```

**Rationale**: Tailwind CSS v4 uses `@theme inline` for custom theme tokens. daisyUI 5 uses the `@plugin "daisyui" { themes: { ... } }` syntax. The `update-apply` theme name will be referenced in the HTML tag.

### Step 1.2 — Install Fonts (Inter + DM Serif Display)

**Run in terminal** at `frontend/web/`:

```bash
pnpm add @fontsource/inter @fontsource/dm-serif-display
```

**Why these fonts**: See THEME_SPECIFICATION.md §3. The serif heading + sans body pairing signals authority with approachability.

### Step 1.3 — Update Root Layout to Use Theme and Fonts

**File**: `app/layout.tsx`

Replace the entire file. Add:
1. Import Inter and DM Serif Display from `@fontsource/*`
2. Set `data-theme="update-apply"` on the `<html>` tag
3. Apply font classes: `font-heading` for headings, `font-sans` for body

```tsx
import type { Metadata } from "next";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/dm-serif-display/400.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "UpdateApply",
  description:
    "Stop rewriting your resume for every job. Connect your repos, we'll match you to jobs and tailor your resume — automatically.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-theme="update-apply" className="h-full">
      <body className="min-h-full flex flex-col bg-base-200 text-base-content font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
```

**Rules**:
- `data-theme="update-apply"` activates our custom daisyUI palette site-wide
- `bg-base-200` applies the warm off-white background globally
- `text-base-content` ensures the warm charcoal text color throughout
- Do NOT remove `antialiased` — it improves font rendering on high-DPI screens

### Step 1.4 — Verify Theme Is Applied

**Run**:

```bash
pnpm dev
```

Visit `http://localhost:3000`. Open DevTools → Elements tab. Verify:
- `<html>` has `data-theme="update-apply"` attribute
- Body background is `#F8F6F3` (warm off-white)
- Any `<button class="btn btn-primary">` renders with navy (`#1E3A5F`) background

---

## Phase 2: API Client Layer

**Goal**: Create the centralized API client that all components will use to talk to the backend. This must exist before any interactive component is built.

### Step 2.1 — Create Directory Structure

```bash
mkdir -p lib/api
```

### Step 2.2 — Create `lib/api/client.ts`

```ts
// lib/api/client.ts
// Base fetch wrapper — single source of truth for all backend API calls.

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
};

type ApiError = {
  status: number;
  message: string;
  details?: unknown;
};

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const { method = "GET", body, headers = {} } = options;

    const fetchHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      ...headers,
    };

    // If running on the client, attach Clerk auth token.
    // On the server, tokens are injected by the calling code.
    if (typeof window !== "undefined") {
      try {
        const { getToken } = await import("@clerk/nextjs");
        const token = await getToken();
        if (token) {
          fetchHeaders["Authorization"] = `Bearer ${token}`;
        }
      } catch {
        // Clerk not available — caller must handle auth themselves
      }
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: fetchHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error: ApiError = {
        status: response.status,
        message: await response.text().catch(() => "Unknown error"),
      };
      throw error;
    }

    return response.json() as Promise<T>;
  }

  get<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "GET" });
  }

  post<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "POST", body });
  }

  put<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "PUT", body });
  }

  patch<T>(path: string, body?: unknown): Promise<T> {
    return this.request<T>(path, { method: "PATCH", body });
  }

  delete<T>(path: string): Promise<T> {
    return this.request<T>(path, { method: "DELETE" });
  }
}

export const apiClient = new ApiClient();
```

### Step 2.3 — Create `lib/api/user.ts`

```ts
// lib/api/user.ts
import { apiClient } from "./client";

export type UserProfile = {
  id: string;
  email: string;
  full_name?: string;
  occupation?: string;
  location?: string;
  created_at: string;
};

export async function createUser(data: {
  email: string;
  full_name?: string;
}): Promise<UserProfile> {
  return apiClient.post<UserProfile>("/user/", data);
}

export async function getUser(id: string): Promise<UserProfile> {
  return apiClient.get<UserProfile>(`/user/${id}`);
}

export async function updateProfile(
  id: string,
  data: Partial<Pick<UserProfile, "full_name" | "occupation" | "location">>
): Promise<UserProfile> {
  return apiClient.patch<UserProfile>(`/user/${id}`, data);
}
```

### Step 2.4 — Create `lib/api/jobs.ts`

```ts
// lib/api/jobs.ts
import { apiClient } from "./client";

export type JobMatch = {
  id: string;
  title: string;
  company: string;
  match_score: number;
  location?: string;
  posted_at: string;
};

export type JobDetail = JobMatch & {
  description: string;
  requirements: string[];
};

export async function getMatches(): Promise<JobMatch[]> {
  return apiClient.get<JobMatch[]>("/jobs/matches");
}

export async function getJobDetail(id: string): Promise<JobDetail> {
  return apiClient.get<JobDetail>(`/jobs/${id}`);
}

export async function generateResume(jobId: string): Promise<{ resume_url: string }> {
  return apiClient.post<{ resume_url: string }>(`/jobs/${jobId}/resume`);
}
```

---

## Phase 3: Layout Components (Header + Footer)

**Goal**: Build the shared layout shell that every page will use. These are Server Components — no `"use client"`.

### Step 3.1 — Create `components/layout/header.tsx`

```tsx
// components/layout/header.tsx
// Server Component — no "use client".
// Navigation bar used on landing page (public) and interior pages (protected).

import Link from "next/link";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Dashboard" },
] as const;

export function Header() {
  return (
    <header className="navbar bg-base-100 shadow-sm sticky top-0 z-50">
      <div className="navbar-start">
        <Link href="/" className="font-heading text-xl text-primary">
          UpdateApply
        </Link>
      </div>

      {/* Desktop nav — hidden on mobile */}
      <nav className="navbar-center hidden lg:flex" aria-label="Main navigation">
        <ul className="menu menu-horizontal px-1 gap-1">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className="text-base-content/80 hover:text-primary transition-colors duration-150"
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Right side — auth CTAs */}
      <div className="navbar-end gap-2">
        <Link href="/sign-in" className="btn btn-ghost btn-sm">
          Sign In
        </Link>
        <Link href="/sign-up" className="btn btn-primary btn-sm">
          Get Started
        </Link>
      </div>

      {/* Mobile hamburger — visible only below lg */}
      <div className="dropdown dropdown-end lg:hidden">
        <label tabIndex={0} className="btn btn-ghost btn-sm" aria-label="Open menu">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </label>
        <ul tabIndex={0} className="menu dropdown-content mt-3 z-[1] p-2 shadow-lg bg-base-100 rounded-box w-52">
          {NAV_LINKS.map((link) => (
            <li key={link.href}>
              <Link href={link.href} className="text-base-content">
                {link.label}
              </Link>
            </li>
          ))}
          <li className="mt-2 border-t border-neutral pt-2">
            <Link href="/sign-in" className="text-base-content">
              Sign In
            </Link>
          </li>
          <li>
            <Link href="/sign-up" className="btn btn-primary btn-sm mt-1 w-full">
              Get Started
            </Link>
          </li>
        </ul>
      </div>
    </header>
  );
}
```

**Design rules applied**:
- `font-heading text-xl text-primary` — serif font, navy color for the logo
- `bg-base-100` — white navbar over the warm off-white page background
- `shadow-sm` — subtle separation from content
- `btn btn-primary` — navy CTA button
- Mobile hamburger uses daisyUI `dropdown` pattern with `lg:hidden`
- All interactive elements have clear hover states (`hover:text-primary`, `duration-150`)
- No emoji, no icon fonts, no `dangerouslySetInnerHTML`

### Step 3.2 — Create `components/layout/footer.tsx`

```tsx
// components/layout/footer.tsx
// Server Component.

import Link from "next/link";

const FOOTER_LINKS = {
  Product: [
    { href: "/features", label: "Features" },
    { href: "/pricing", label: "Pricing" },
  ],
  Support: [
    { href: "/contact", label: "Contact" },
    { href: "/faq", label: "FAQ" },
  ],
  Legal: [
    { href: "/privacy", label: "Privacy Policy" },
    { href: "/terms", label: "Terms of Service" },
  ],
} as const;

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer bg-base-100 border-t border-neutral px-6 py-12 lg:footer-horizontal">
      <nav>
        <header className="footer-title text-base-content">Product</header>
        {FOOTER_LINKS.Product.map((link) => (
          <Link key={link.href} href={link.href} className="link link-hover text-base-content/70">
            {link.label}
          </Link>
        ))}
      </nav>
      <nav>
        <header className="footer-title text-base-content">Support</header>
        {FOOTER_LINKS.Support.map((link) => (
          <Link key={link.href} href={link.href} className="link link-hover text-base-content/70">
            {link.label}
          </Link>
        ))}
      </nav>
      <nav>
        <header className="footer-title text-base-content">Legal</header>
        {FOOTER_LINKS.Legal.map((link) => (
          <Link key={link.href} href={link.href} className="link link-hover text-base-content/70">
            {link.label}
          </Link>
        ))}
      </nav>
      <nav className="lg:ml-auto">
        <header className="footer-title text-base-content">UpdateApply</header>
        <p className="text-base-content/60 text-sm">
          &copy; {currentYear} UpdateApply. All rights reserved.
        </p>
      </nav>
    </footer>
  );
}
```

**Design rules applied**:
- `footer` + `lg:footer-horizontal` — daisyUI's responsive footer pattern
- `bg-base-100` — white footer matching the header
- `border-t border-neutral` — warm gray top border for separation
- `link link-hover` — daisyUI's styled link with underline-on-hover
- No emoji in link labels or headings

---

## Phase 4: Landing Page Components

**Goal**: Build each section of the landing page as an independent Server Component, then compose them in `app/page.tsx`.

### Important Rule for ALL Components

These are **Server Components** by default. Do NOT add `"use client"` unless you need:
- Browser APIs (`window`, `localStorage`, etc.)
- Event handlers (`onClick`, `onSubmit`, etc.)
- React hooks (`useState`, `useEffect`, etc.)

The landing page is **static content**. It needs zero client-side JavaScript for rendering.

### Step 4.1 — Create `components/landing/hero.tsx`

```tsx
// components/landing/hero.tsx
// Server Component.

export function Hero() {
  return (
    <section className="hero min-h-[85vh] bg-base-200">
      <div className="hero-content flex-col lg:flex-row-reverse gap-12 max-w-6xl">
        {/* Visual element — subtle illustration area */}
        <div className="lg:w-1/2 flex items-center justify-center">
          <div className="w-72 h-72 rounded-full bg-gradient-to-br from-primary/10 via-accent/10 to-secondary/10" />
        </div>

        {/* Text content */}
        <div className="lg:w-1/2 text-center lg:text-left">
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl text-primary leading-tight">
            Stop rewriting your resume for every job.
          </h1>
          <p className="py-6 text-base md:text-lg text-base-content/80 max-w-prose">
            Connect your repos. We&apos;ll match you to jobs and tailor your resume — automatically.
          </p>

          {/* Primary CTA */}
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <a href="/sign-up" className="btn btn-primary btn-lg text-base px-8">
              Get Started Free
            </a>
            <span className="text-sm text-base-content/60">No credit card required</span>
          </div>

          {/* Provider badges */}
          <div className="mt-8 flex flex-wrap items-center justify-center lg:justify-start gap-4 text-sm text-base-content/60">
            <span className="text-xs uppercase tracking-widest">Connect your work</span>
            <div className="flex gap-3">
              {["GitHub", "Google Drive", "Notion"].map((name) => (
                <span
                  key={name}
                  className="badge badge-outline badge-lg text-base-content/70 px-4 py-3"
                >
                  {name}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
```

**Design rules applied**:
- `hero` + `hero-content` — daisyUI's purpose-built hero layout
- `bg-base-200` — warm off-white section background
- `font-heading` — serif font for the main headline
- `text-primary` — navy headline that signals authority
- `btn btn-primary btn-lg` — navy CTA button
- `badge badge-outline badge-lg` — provider badges in outline style
- `max-w-prose` — comfortable reading width on body text
- Responsive: `flex-col lg:flex-row-reverse`, `text-center lg:text-left`
- **No emoji** in badges or anywhere else

### Step 4.2 — Create `components/landing/how-it-works.tsx`

```tsx
// components/landing/how-it-works.tsx
// Server Component.

const STEPS = [
  {
    number: "01",
    title: "Connect",
    description: "Link your GitHub, Google Drive, and Notion. One connection, and we start building your profile from your actual work.",
  },
  {
    number: "02",
    title: "Extract",
    description: "We read your repos and documents to understand your skills, projects, and experience. No forms, no manual data entry.",
  },
  {
    number: "03",
    title: "Apply",
    description: "We match you to jobs that fit your stack and generate a tailored resume for every application — from scratch, for that specific role.",
  },
];

export function HowItWorks() {
  return (
    <section className="py-20 px-6 bg-base-100">
      <div className="max-w-5xl mx-auto">
        <h2 className="font-heading text-3xl md:text-4xl text-primary text-center mb-4">
          How It Works
        </h2>
        <p className="text-base-content/70 text-center max-w-lg mx-auto mb-16 text-base md:text-lg">
          Three steps from connection to application. No noise, no busywork.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          {STEPS.map((step, index) => (
            <article key={step.number} className="text-center relative">
              {/* Step number */}
              <div className="w-14 h-14 rounded-full bg-primary text-primary-content flex items-center justify-center mx-auto mb-5 font-heading text-xl">
                {step.number}
              </div>
              {/* Connector line (desktop only) */}
              {index < STEPS.length - 1 && (
                <div className="hidden md:block absolute top-7 left-[60%] w-[80%] h-px bg-neutral" />
              )}
              <h3 className="font-heading text-xl text-primary mb-3">{step.title}</h3>
              <p className="text-base-content/70 text-sm leading-relaxed max-w-xs mx-auto">
                {step.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Design rules applied**:
- `bg-base-100` — white section alternating with adjacent sections
- `font-heading text-primary` — serif navy headings consistently
- `grid-cols-1 md:grid-cols-3` — responsive grid (stacks on mobile)
- Numbered circles in `bg-primary text-primary-content` — navy circles with white numbers
- Connection line between steps using `h-px bg-neutral` (visible on desktop only)
- No emoji, no icons for step indicators — clean numbered approach

### Step 4.3 — Create `components/landing/features.tsx`

```tsx
// components/landing/features.tsx
// Server Component.

const FEATURES = [
  {
    title: "Zero Data Entry",
    description:
      "Your profile builds itself from the work you have already done. Link your repos, and we surface your skills, projects, and experience — no tedious forms, no manual copying.",
  },
  {
    title: "One-Click Matching",
    description:
      "We scan thousands of live job postings and surface the ones that genuinely fit your background. Stop scrolling — start applying.",
  },
  {
    title: "Perfect Fit, Every Time",
    description:
      "Each resume is crafted from scratch to speak directly to the role you are applying for. Highlight the right experience, use the right language, make every application count.",
  },
  {
    title: "Always Synced",
    description:
      "Update your code, update your docs — your profile stays current everywhere. One sync keeps your entire application arsenal fresh.",
  },
  {
    title: "Smarter Over Time",
    description:
      "The more you use UpdateApply, the better it learns what makes you stand out. Better matches, stronger resumes, less friction — with every cycle.",
  },
  {
    title: "Privacy First",
    description:
      "We access your files to understand your work — we never share them. You are in control of what gets connected and when.",
  },
];

export function Features() {
  return (
    <section className="py-20 px-6 bg-base-200">
      <div className="max-w-6xl mx-auto">
        <h2 className="font-heading text-3xl md:text-4xl text-primary text-center mb-4">
          Your Career, on Autopilot
        </h2>
        <p className="text-base-content/70 text-center max-w-lg mx-auto mb-16 text-base md:text-lg">
          Six ways UpdateApply takes the friction out of your job search.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature) => (
            <article
              key={feature.title}
              className="card bg-base-100 shadow-md border border-neutral/50"
            >
              <div className="card-body">
                <h3 className="card-title font-heading text-lg text-primary">
                  {feature.title}
                </h3>
                <p className="text-base-content/70 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Design rules applied**:
- `card bg-base-100 shadow-md border border-neutral/50` — white cards with subtle warm-gray border and soft shadow
- `card-body` + `card-title` — daisyUI's card system
- `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` — responsive grid stacking on mobile
- `bg-base-200` — warm off-white section background (alternates with white sections)
- Feature descriptions use `text-base-content/70` — reduced opacity for secondary text
- No emoji, no icons in feature cards (per THEME_SPECIFICATION §4 — line-art SVG only)
- Each feature card is an `<article>` for semantic HTML

### Step 4.4 — Create `components/landing/providers.tsx`

```tsx
// components/landing/providers.tsx
// Server Component.

const PROVIDERS = [
  {
    name: "GitHub",
    description: "Connect your repos, PRs, and contributions",
  },
  {
    name: "Google Drive",
    description: "Import your existing work and project documents",
  },
  {
    name: "Notion",
    description: "Pull your career notes and project docs",
  },
];

export function Providers() {
  return (
    <section className="py-20 px-6 bg-base-100">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="font-heading text-3xl md:text-4xl text-primary mb-4">
          Supported Platforms
        </h2>
        <p className="text-base-content/70 max-w-md mx-auto mb-12 text-base md:text-lg">
          Connect the tools you already use. We read your work where it lives.
        </p>

        <div className="flex flex-wrap justify-center gap-6">
          {PROVIDERS.map((provider) => (
            <article
              key={provider.name}
              className="card bg-base-200 shadow-sm border border-neutral/50 w-64"
            >
              <div className="card-body items-center text-center py-8">
                {/* Placeholder for SVG icon — to be replaced with actual SVG component */}
                <div className="w-14 h-14 rounded-full bg-primary/5 border border-primary/10 flex items-center justify-center mb-4">
                  <span className="font-heading text-sm text-primary">{provider.name.charAt(0)}</span>
                </div>
                <h3 className="card-title font-heading text-base text-primary">
                  {provider.name}
                </h3>
                <p className="text-base-content/60 text-sm">
                  {provider.description}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Design rules applied**:
- Cards in `bg-base-200` (subtle contrast from the white section background)
- Placeholder circle for provider icon — to be replaced with actual SVG component later
- `border-primary/10` — subtle tinted border that hints at the primary color
- Centered content for visual consistency
- No provider logos yet — these come from `public/icons/` when SVGs are provided

### Step 4.5 — Create `components/landing/cta-section.tsx`

```tsx
// components/landing/cta-section.tsx
// Server Component.

export function CtaSection() {
  return (
    <section className="py-24 px-6 bg-primary">
      <div className="max-w-3xl mx-auto text-center">
        <h2 className="font-heading text-3xl md:text-4xl text-primary-content mb-4">
          Ready to stop rewriting?
        </h2>
        <p className="text-primary-content/80 max-w-lg mx-auto mb-10 text-base md:text-lg">
          Join UpdateApply and let your work speak for itself. Your next opportunity is one connection away.
        </p>
        <a
          href="/sign-up"
          className="btn btn-lg bg-secondary text-secondary-content border-none hover:opacity-90 text-base px-10"
        >
          Get Started Free
        </a>
        <p className="text-primary-content/60 text-sm mt-4">
          No credit card required
        </p>
      </div>
    </section>
  );
}
```

**Design rules applied**:
- `bg-primary` — full navy background section (visual break from the alternating white/warm-off-white)
- `btn bg-secondary text-secondary-content` — amber CTA button on navy background for maximum contrast and visual pop
- `text-primary-content` — white text on navy background
- `/60`, `/80` opacity variants for hierarchy
- Minimalist layout — headline, subheadline, single CTA, fine-print reassurance

### Step 4.6 — Assemble Landing Page in `app/page.tsx`

```tsx
// app/page.tsx
// Server Component — composes all landing sections.

import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { Hero } from "@/components/landing/hero";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Features } from "@/components/landing/features";
import { Providers } from "@/components/landing/providers";
import { CtaSection } from "@/components/landing/cta-section";

export default function Home() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <HowItWorks />
        <Features />
        <Providers />
        <CtaSection />
      </main>
      <Footer />
    </>
  );
}
```

**Rules applied**:
- Page is a Server Component — zero client JS for rendering
- Sections are composed in order: Hero → How It Works → Features → Providers → CTA
- `Header` and `Footer` wrap the main content
- Each section is an independent component file (one concern per file, §4.2 of PM Plan)
- No inline styles, no `dangerouslySetInnerHTML`

### Step 4.7 — Set Up Path Aliases

**File**: `tsconfig.json`

Verify that `@/*` maps to `./*`:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

This is needed for the `@/components/...` imports. Next.js usually adds this by default, but verify it exists.

---

## Phase 5: Authentication (Clerk)

**Goal**: Add authentication so "Get Started Free" and "Sign In" actions actually work.

### Step 5.1 — Install Clerk

```bash
pnpm add @clerk/nextjs
```

### Step 5.2 — Add Environment Variables

Create `.env.local` in `frontend/web/` (this file is gitignored — never commit it):

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Replace the key values** with actual Clerk credentials from the Clerk Dashboard.

### Step 5.3 — Register Clerk Middleware

Create `middleware.ts` in `frontend/web/`:

```ts
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher(["/dashboard(.*)", "/resume(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
};
```

### Step 5.4 — Wrap Layout with ClerkProvider

Update `app/layout.tsx` to wrap with ClerkProvider:

```tsx
import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/inter/700.css";
import "@fontsource/dm-serif-display/400.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "UpdateApply",
  description:
    "Stop rewriting your resume for every job. Connect your repos, we'll match you to jobs and tailor your resume — automatically.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" data-theme="update-apply" className="h-full">
        <body className="min-h-full flex flex-col bg-base-200 text-base-content font-sans antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

### Step 5.5 — Update Header with Clerk Auth Buttons

**File**: `components/layout/header.tsx`

Replace the static "Sign In" / "Get Started" buttons with Clerk's `<SignInButton />` and `<SignUpButton />`. To keep Header as a Server Component, extract the auth portion into a small client component.

Create `components/layout/auth-section.tsx`:

```tsx
"use client";
import { SignInButton, SignUpButton, UserButton, useAuth } from "@clerk/nextjs";

export function AuthSection() {
  const { isSignedIn } = useAuth();

  if (isSignedIn) {
    return <UserButton afterSignOutUrl="/" />;
  }

  return (
    <>
      <SignInButton mode="modal">
        <button className="btn btn-ghost btn-sm">Sign In</button>
      </SignInButton>
      <SignUpButton mode="modal">
        <button className="btn btn-primary btn-sm">Get Started</button>
      </SignUpButton>
    </>
  );
}
```

Then in `header.tsx`, import `<AuthSection />` and replace the `navbar-end` div's contents with it:

```tsx
import { AuthSection } from "./auth-section";

// Inside the header, replace the navbar-end children:
<div className="navbar-end gap-2">
  <AuthSection />
</div>
```

And similarly in the mobile dropdown menu.

**Important**: Keep `header.tsx` as a Server Component. Only `AuthSection` needs `"use client"`.

---

## Phase 6: Onboarding Wizard (Post-Sign-Up Flow)

**Goal**: Guide first-time users through connecting providers and setting up their profile.

This phase is documented here at a high level. A detailed implementation plan will be created separately.

**Key components to build**:
- `app/(auth)/onboarding/page.tsx` — Multi-step wizard wrapper
- `components/shared/provider-button.tsx` — Reusable provider connection button
- `components/shared/profile-form.tsx` — Form for occupation, location, preferences

**Design rules for onboarding**:
- Use daisyUI `steps` component for progress indication
- Use `step-primary` for completed/current steps
- Keep each step focused on ONE action — never show multiple unrelated fields
- daisyUI `input` + `label` for form fields (not shadcn — daisyUI is sufficient here)
- `btn btn-primary` for "Next" / "Complete" actions
- `btn btn-ghost` for "Skip" links

---

## Phase 7: Dashboard (Protected)

**Goal**: The post-authentication home where users see job matches, profile status, and take action.

This is documented here as a roadmap. A detailed implementation plan will be created separately.

**Key components to build**:
- `components/layout/sidebar.tsx` — daisyUI `drawer` with `lg:drawer-open`
- `components/shared/job-card.tsx` — Reusable job match card with match score
- `components/shared/match-score.tsx` — Visual match percentage indicator

**Design rules for dashboard**:
- daisyUI `drawer` for sidebar with `lg:drawer-open` (collapses to overlay on mobile)
- `menu` component for sidebar navigation items
- `card` grid for job matches: `grid-cols-1 md:grid-cols-2 xl:grid-cols-3`
- Match score displayed using `radial-progress` or `badge` in `secondary` (amber) color
- `btn btn-primary` for "Generate Resume" actions
- `skeleton` loading states while data fetches

---

## Component Design Rules (Must Follow)

These rules apply to **every component** you build. Violations will be sent back for rework.

### Rule 1: Color Usage

| Token | When to Use | When NOT to Use |
|-------|-------------|-----------------|
| `bg-primary` / `text-primary` | Headlines, primary CTAs, logo, active states | Body text, secondary content, backgrounds of feature cards |
| `bg-secondary` / `text-secondary` | Highlights, badges, match scores, accent CTAs on dark backgrounds | Full-page backgrounds, primary navigation |
| `bg-accent` / `text-accent` | Dividers, borders, secondary visual elements | Buttons, CTAs, navigation |
| `bg-base-200` | Section backgrounds (alternating with base-100) | Cards, elevated surfaces |
| `bg-base-100` | Cards, navbars, footers, elevated surfaces | Full-page backgrounds |
| `base-content/70` or `base-content/60` | Body text, descriptions, secondary info | Headlines, primary labels |
| `neutral` | Borders, dividers, horizontal rules | Text, backgrounds |

### Rule 2: Typography

- **Headings**: Always use `font-heading` class (serif). Never use `font-sans` for h1–h3.
- **Body text**: Always use `font-sans` class (inherited from `<body>` unless overridden).
- **Never skip heading levels**: h1 → h2 → h3. No h1 → h3.
- **Responsive sizes**: Use pattern `text-3xl md:text-4xl lg:text-5xl` for h1, `text-xl md:text-2xl` for h2, etc.
- **Line length**: Keep body text at `max-w-prose` or `max-w-lg` for readability.

### Rule 3: Icons & Emoji

- **Zero emoji** in the UI. Re-read §7.1 of the PM Plan if unclear.
- Icons must be inline SVG components (not `<img>` tags) so they inherit stroke color.
- Icon components must accept a `className` prop.
- Placeholder circles (like the letter-initial approach in `providers.tsx`) are acceptable until real SVGs arrive.

### Rule 4: Buttons

- Primary actions: `btn btn-primary`
- Secondary actions: `btn btn-outline` or `btn btn-ghost`
- Large buttons: add `btn-lg`
- Small buttons: add `btn-sm`
- Full-width on mobile: add `w-full sm:w-auto`
- **Never** use a `<div>` or `<span>` as a button. Use `<button>` or `<Link>`.

### Rule 5: Cards

- Always use daisyUI's `card` class, not a custom wrapper.
- Structure: `card` > `card-body` > `card-title` + content.
- Use `shadow-md` for elevated cards, no shadow for flat cards.
- Use `border border-neutral/50` for subtle card boundaries.

### Rule 6: Animation & Motion

| Allowed | Not Allowed |
|---------|-------------|
| Subtle color transitions (`duration-150 hover:opacity-90`) | Spin, bounce, pulse animations |
| Fade-in on scroll (Intersection Observer, no library) | Flying, sliding, parallax effects |
| daisyUI skeleton loading states | Custom CSS keyframe animations |
| daisyUI loading spinners for inline actions | Full-page loading animations |

- Always respect `prefers-reduced-motion`: daisyUI does this by default.

### Rule 7: Responsive Layout

- Every section must work at 320px, 768px, and 1440px.
- Test BEFORE marking complete.
- Mobile-first classes: `flex-col lg:flex-row`, `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`.
- No horizontal scroll at any breakpoint.

---

## File Tree (What Should Exist After Implementation)

```
frontend/web/
├── app/
│   ├── globals.css              ← Custom daisyUI "update-apply" theme
│   ├── layout.tsx               ← ClerkProvider + data-theme + fonts
│   ├── middleware.ts             ← Clerk route protection
│   ├── page.tsx                  ← Landing page composition
│   ├── dashboard/
│   │   └── page.tsx              ← Dashboard placeholder (enhanced later)
│   └── (auth)/
│       └── callback/
│           └── page.tsx          ← Create if Clerk requires it
│
├── components/
│   ├── landing/
│   │   ├── hero.tsx              ← Hero section
│   │   ├── how-it-works.tsx      ← 3-step process
│   │   ├── features.tsx          ← 6 benefit cards
│   │   ├── providers.tsx         ← Platform cards
│   │   └── cta-section.tsx       ← Final CTA
│   ├── layout/
│   │   ├── header.tsx            ← Navbar (Server Component)
│   │   ├── auth-section.tsx      ← Clerk buttons (Client Component)
│   │   └── footer.tsx            ← Footer (Server Component)
│   └── providers/                ← (future: SVG icon wrappers)
│       ├── github-icon.tsx
│       ├── google-drive-icon.tsx
│       └── notion-icon.tsx
│
├── lib/
│   ├── api/
│   │   ├── client.ts             ← Base fetch wrapper
│   │   ├── user.ts               ← User endpoints
│   │   └── jobs.ts               ← Job endpoints
│   └── utils.ts                  ← (future: shared utilities)
│
├── .env.local                    ← Clerk keys + API URL (gitignored)
├── postcss.config.mjs            ← Already exists, no changes
├── next.config.ts                ← Already exists, no changes
├── package.json                  ← Already exists, no changes
└── tsconfig.json                 ← Verify @/ path alias exists
```

---

## Implementation Order (Summary)

| Order | Phase | Key Files | Depends On |
|-------|-------|-----------|------------|
| 1 | Theme Foundation | `globals.css`, `layout.tsx` | Nothing |
| 2 | API Client | `lib/api/client.ts`, `user.ts`, `jobs.ts` | Nothing (parallel with Phase 1) |
| 3 | Layout Components | `header.tsx`, `footer.tsx` | Phase 1 |
| 4 | Landing Page | `hero.tsx`, `how-it-works.tsx`, `features.tsx`, `providers.tsx`, `cta-section.tsx`, `page.tsx` | Phase 3 |
| 5 | Auth | `middleware.ts`, `auth-section.tsx`, `.env.local` | Phase 1 |
| 6 | Onboarding | `onboarding/page.tsx`, `provider-button.tsx`, `profile-form.tsx` | Phase 5 |
| 7 | Dashboard | `sidebar.tsx`, `job-card.tsx`, `match-score.tsx` | Phase 5 |

**Parallelism**: Phases 1 and 2 can run in parallel. Everything else is sequential.

---

## Verification Checklist (Run Before Marking Complete)

### Phase 1 — Theme
- [ ] `<html>` tag has `data-theme="update-apply"`
- [ ] Body background is `#F8F6F3` (warm off-white)
- [ ] `btn btn-primary` renders with navy (`#1E3A5F`) background
- [ ] Inter font loads for body text
- [ ] DM Serif Display font loads for headings

### Phase 2 — API Client
- [ ] `apiClient.get<T>()` compiles with TypeScript strict mode
- [ ] Error responses are caught and typed as `ApiError`
- [ ] No hardcoded `fetch` calls in components (all go through client)

### Phase 3 — Layout
- [ ] Header renders at top of landing page
- [ ] Footer renders at bottom with all three link columns
- [ ] Mobile hamburger menu appears below 1024px
- [ ] All links are keyboard-navigable (Tab key)
- [ ] Header has `aria-label="Main navigation"` on desktop nav

### Phase 4 — Landing Page
- [ ] All 5 sections render in correct order
- [ ] Page is fully responsive at 320px, 768px, 1440px
- [ ] No horizontal scroll at any breakpoint
- [ ] Touch targets ≥44×44px on mobile
- [ ] Heading hierarchy: one `<h1>`, multiple `<h2>`, `<h3>` as needed
- [ ] No emoji anywhere
- [ ] Semantic HTML: `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>`
- [ ] No `"use client"` directive on any landing component
- [ ] Lighthouse Performance ≥ 90
- [ ] Total JS bundle < 200 KB gzipped

### Phase 5 — Auth
- [ ] `/dashboard` redirects unauthenticated users to sign-in
- [ ] Landing page is public (no auth required)
- [ ] Sign Up modal opens when clicking "Get Started Free"
- [ ] After sign-up, user is redirected to `/onboarding` or `/dashboard`
- [ ] No Clerk tokens stored in localStorage or sessionStorage

---

## Excluded from Current Scope

| Feature | Reason | Future Phase |
|---------|--------|-------------|
| Dark mode | Not in MVP. daisyUI supports `data-theme` toggle when needed. | Post-MVP |
| shadcn components | Not needed yet. Landing page is pure daisyUI. Only install when complex interactions arise (Phase 6: Onboarding wizard validation). | Phase 6+ |
| Provider SVG icons | User will provide SVG assets. Until then, placeholder initials are acceptable. | Phase 6 |
| Lottie animations | No Lottie files provided yet. | Post-MVP |
| Dashboard full implementation | Only the auth infrastructure is set up here. Dashboard content components come in a separate plan. | Dedicated dashboard plan |
| Resume generation page | Depends on dashboard and backend integration. | Dedicated resume plan |
| Unit tests / E2E tests | Will be introduced in a later quality phase. | Post-MVP |

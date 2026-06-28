# Landing Page Design — UpdateApply

## Current State

| Area | Status |
|------|--------|
| **Landing page** (`/`) | Bare-bones — just "Welcome to UpdateApply" + a link to `/dashboard` |
| **Dashboard** (`/dashboard`) | Empty placeholder |
| **Styling** | Tailwind CSS 4 + daisyUI 5 — ready to use |
| **Auth** | Clerk is called out in the design doc but not yet integrated |
| **Backend** | Has user CRUD, job profile CRUD, job post model — but no frontend hooks it up yet |

---

## 1. Hero Section (Above the Fold)

The first thing a visitor sees. Communicates the value proposition instantly.

```
┌──────────────────────────────────────────────────────┐
│  [Logo] UpdateApply                           [Get Started] │
│                                                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │                                                  │       │
│  │   Stop rewriting your resume for every job.      │       │
│  │                                                  │       │
│  │   Connect your repos. We'll match you to jobs    │       │
│  │   and tailor your resume — automatically.        │       │
│  │                                                  │       │
│  │        [Get Started Free →]                      │       │
│  │        No credit card required                   │       │
│  │                                                  │       │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐        │       │
│  │   │ GitHub   │ │ GDrive   │ │ Notion   │        │       │
│  │   └──────────┘ └──────────┘ └──────────┘        │       │
│  │   Connect your work repositories                 │       │
│  └──────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────┘
```

- **Headline**: "Stop rewriting your resume for every job."
- **Subheadline**: Explains the one-click value prop.
- **Primary CTA**: "Get Started Free" → triggers Clerk sign-up modal.
- **Provider badges**: GitHub, Google Drive, Notion logos (visual trust signals).

---

## 2. How It Works (3-Step Process)

Mirrors the core user flow — Connect → Extract → Match & Generate.

```
┌──────────────────────────────────────────────────────┐
│              How It Works                            │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │    1     │    │    2     │    │    3     │      │
│  │  Connect │───►│ Extract  │───►│  Apply   │      │
│  │          │    │          │    │          │      │
│  │ Link your │   │ We read  │   │ We match │      │
│  │ GitHub,   │   │ your     │   │ you to   │      │
│  │ Drive, &  │   │ repos &  │   │ jobs &   │      │
│  │ Notion    │   │ build    │   │ generate │      │
│  │           │   │ your     │   │ tailored │      │
│  │           │   │ profile  │   │ resumes  │      │
│  └──────────┘    └──────────┘    └──────────┘      │
└──────────────────────────────────────────────────────┘
```

Each step rendered as an animated card or icon block.

---

## 3. Features / Benefits Section

Benefit-driven cards. No implementation jargon — just outcomes.

```
┌────────────────────────────────────────────────────────────┐
│        Your Career, On Autopilot                          │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  🚀          │  │  ⚡          │  │  🎯          │    │
│  │  Zero Data   │  │  One-Click   │  │  Perfect     │    │
│  │  Entry       │  │  Matching    │  │  Fit, Every  │    │
│  │              │  │              │  │  Time        │    │
│  │  Your profile │  │  We surface  │  │  Every resume│    │
│  │  builds itself│  │  roles that  │  │  is written  │    │
│  │  from the     │  │  actually    │  │  from the    │    │
│  │  work you've  │  │  fit your    │  │  ground up   │    │
│  │  already done.│  │  stack.      │  │  for that    │    │
│  │  No forms.    │  │  No noise.   │  │  specific    │    │
│  │  No fuss.     │  │              │  │  role.       │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  🔗          │  │  📈          │  │  🛡️          │    │
│  │  Always      │  │  Smarter     │  │  Privacy     │    │
│  │  Synced      │  │  Over Time   │  │  First       │    │
│  │              │  │              │  │              │    │
│  │  Connect once.│  │  The more    │  │  Your data   │    │
│  │  Your profile │  │  you use it, │  │  stays yours.│    │
│  │  stays fresh  │  │  the better  │  │  We read,    │    │
│  │  across all   │  │  your matches│  │  we don't    │    │
│  │  platforms.   │  │  and resumes │  │  store.      │    │
│  │               │  │  become.     │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────────────────────────────────────┘
```

### Benefit Cards — Copy Detail

| Headline | Body Copy |
|----------|-----------|
| 🚀 **Zero Data Entry** | Your profile builds itself from the work you've already done. Link your repos, and we surface your skills, projects, and experience — no tedious forms, no manual copying. |
| ⚡ **One-Click Matching** | We scan thousands of live job postings and surface the ones that genuinely fit your background. Stop scrolling — start applying. |
| 🎯 **Perfect Fit, Every Time** | Each resume is crafted from scratch to speak directly to the role you're applying for. Highlight the right experience, use the right language, make every application count. |
| 🔗 **Always Synced** | Update your code, update your docs — your profile stays current everywhere. One sync keeps your entire application arsenal fresh. |
| 📈 **Smarter Over Time** | The more you use UpdateApply, the better it learns what makes you stand out. Better matches, stronger resumes, less friction — with every cycle. |
| 🛡️ **Privacy First** | We access your files to understand your work — we never share them. You're in control of what gets connected and when. |

---

## 4. Supported Providers Section

Visual cards/logos for each supported integration:

- **GitHub** — Connect your repos, PRs, and contributions
- **Google Drive** — Import your existing work and project documents
- **Notion** — Pull your career notes and project docs

---

## 5. Dashboard Preview / Teaser

A mockup or screenshot of the dashboard showing:
- Match score cards
- Job listings with "Generate Resume" buttons
- Profile completeness indicator

Gives users a reason to sign up — shows what they're working toward.

---

## 6. Footer

- Links to: Privacy Policy, Terms of Service (placeholder OK)
- Copyright notice
- Social links (GitHub org, etc.)

---

## Technical Considerations

### Authentication Flow

Clerk is used for frontend-side auth. The "Get Started" CTA opens the Clerk `<SignInButton />` or `<SignUpButton />` modal. Once authenticated:

1. Clerk returns the user info.
2. Frontend calls `POST /user/` to create the user in the backend.
3. User is redirected to `/dashboard` or an onboarding wizard.

### Onboarding Flow (Post-Sign-Up)

The landing page CTA leads into a setup wizard:

1. **Step 1 — Connect Providers**: "Link your GitHub / Google Drive / Notion"
2. **Step 2 — Build Your Profile**: Pre-fill from OAuth data, let them set occupation, location, preferences.
3. **Step 3 — Sync Your Repos**: Trigger the backend to pull and process files.
4. **Redirect to Dashboard**: Where matches start appearing.

### Recommended Pages Structure

```
app/
├── page.tsx              ← Landing page
├── layout.tsx            ← Root layout (exists)
├── globals.css           ← Tailwind + daisyUI (exists)
├── (auth)/
│   └── callback/         ← Clerk / OAuth callback handlers
├── dashboard/
│   ├── page.tsx          ← Main dashboard (exists, needs work)
│   ├── matches/
│   │   └── page.tsx      ← Job matches list
│   └── profile/
│       └── page.tsx      ← Edit profile / onboarding
├── resume/
│   └── [id]/
│       └── page.tsx      ← View / download generated resume
```

### Component Architecture

```
components/
├── landing/
│   ├── hero.tsx
│   ├── how-it-works.tsx
│   ├── features.tsx
│   ├── providers.tsx
│   └── cta-section.tsx
├── ui/
│   ├── button.tsx        ← daisyUI btn classes
│   ├── card.tsx          ← daisyUI card
│   └── navbar.tsx
└── providers/
    ├── github-icon.tsx
    ├── google-drive-icon.tsx
    └── notion-icon.tsx
```

---

## What's Missing / Prerequisites

To make the landing page fully functional:

1. **Clerk integration** — Install `@clerk/nextjs`, wrap the layout with `<ClerkProvider>`, add middleware for protected routes.
2. **Backend API client** — A thin service layer (e.g., `fetch` or `openapi-fetch`) to call the FastAPI backend.
3. **Provider icons** — SVG logos for GitHub, Google Drive, Notion.
4. **Onboarding wizard** — Multi-step form for first-time users to set up their profile and connect providers.

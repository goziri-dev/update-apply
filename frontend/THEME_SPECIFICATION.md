# Theme Specification — UpdateApply

> **Author**: Product Manager  
> **Status**: Approved  
> **Scope**: All frontend code in `frontend/web/`

---

## 1. Design Philosophy

We are building for **professionals seeking their next career opportunity** — not for developers building developer tools.

| What we are NOT | What we ARE |
|----------------|-------------|
| Black-and-white shadcn minimalism (too sterile for a personal, high-stakes journey) | **Warm Professional** — like a well-dressed career coach in a comfortable office |
| Futuristic neon / startup hype (too cold, too "we're building infra") | **Trustworthy & supportive** — we've got this, you're in good hands |
| Playful / whimsical (undermines the seriousness of job seeking) | **Clear & calm** — job seeking is confusing enough; we don't add to it |

The user is stressed about their search, juggling applications, networking, and existing work. Every pixel should signal: **competence + care.**

---

## 2. Color Palette

| Token | Hex | Role |
|-------|-----|------|
| **Primary** | `#1E3A5F` | Warm Navy — trust, stability, authority |
| Primary-content | `#FFFFFF` | Crisp contrast on CTAs and primary surfaces |
| **Secondary** | `#D4954E` | Soft Amber — optimism, warmth, "gold" without being gaudy. Use sparingly (accents, badges, highlights). |
| Secondary-content | `#1A1A1A` | Readable text on amber backgrounds |
| **Accent** | `#5B8C7E` | Muted Sage — growth, calm, freshness. Dividers, borders, secondary visual elements. |
| Accent-content | `#FFFFFF` | Contrast for accent surfaces |
| **Background** | `#F8F6F3` | Warm Off-White — like quality paper, not a terminal |
| Base-100 | `#FFFFFF` | Cards and elevated surfaces |
| Base-200 | `#F8F6F3` | Section backgrounds |
| Base-300 | `#EDE9E4` | Subtle contrast surfaces |
| **Base-content** | `#2D2A28` | Warm Charcoal — softer than pure black, easier on the eyes, still high-contrast |
| Neutral | `#E5E0DA` | Warm grays for borders and dividers |
| Neutral-content | `#2D2A28` | Text on neutral surfaces |
| Info | `#6B9BC4` | Informational states |
| Success | `#5B8C7E` | Success states |
| Warning | `#D4954E` | Warning states |
| Error | `#C4544A` | Error states |

### Why These Colors Work Together

| Color | Emotional Signal |
|-------|-----------------|
| **Warm Navy** | *"We are serious, established, and we will land you results."* |
| **Soft Amber** | *"There's opportunity ahead. We're rooting for you."* |
| **Muted Sage** | *"Growth is natural here. Let your career bloom."* |
| **Warm backgrounds** | *"Breathe. This is a supportive space."* |

---

## 3. Typography

| Role | Font | Why |
|------|------|-----|
| **Headings** | Serif (DM Serif Display, Playfair Display, or similar) | Authority, care, craftsmanship — stands out from the SaaS crowd |
| **Body** | Clean sans-serif (Inter, Outfit, or similar) | Modern, highly readable, not distracting |

This pairing signals: *"We have personality AND we're easy to work with."*

### Typography Rules

- Responsive sizes only: `text-sm md:text-base lg:text-lg` pattern
- Generous line-height (`leading-relaxed` or `leading-7`)
- Comfortable max-width on text blocks (`max-w-prose` or `max-w-2xl`)
- Ample vertical whitespace between sections — stressed users need scanability
- Never use fixed `px` font sizes

---

## 4. Visual Style Guidelines

### Buttons (daisyUI `btn`)

| Variant | Style | Hover |
|---------|-------|-------|
| Primary CTA | `btn btn-primary` (Warm Navy bg, white text) | Slightly lighter navy or subtle amber underline/glow |
| Secondary | `btn btn-outline` | Filled on hover |

### Cards (daisyUI `card`)

| Property | Value |
|----------|-------|
| Background | `base-100` (white) |
| Border | Thin warm-gray (`neutral` or `base-300`) |
| Shadow | Subtle (`shadow-md`) |
| Border radius | daisyUI default (respects theme) |

### Icons

- **Line-art SVG only** — no filled/colored illustrations
- Stroke color inherits from text color (navy, warm charcoal, or sage)
- Absolutely **no emoji** anywhere in the UI (per PM Plan §7.1)
- Icon components accept `className` for size/color overrides

### Dividers & Borders

- Use `divider` component from daisyUI with neutral color
- Thin, unobtrusive — guides the eye without adding visual noise

### Loading States

- daisyUI `skeleton` with warm gray tones
- daisyUI `loading` spinner for inline actions
- Both respect `prefers-reduced-motion`

---

## 5. Animation Philosophy

| Guideline | Rationale |
|-----------|-----------|
| **Minimal** | Job seekers don't need spectacle. They need clarity. |
| **Respect `prefers-reduced-motion`** | daisyUI 5.6 supports this natively for loading animations |
| **No spin / bounce / fly** | Nothing that distracts or creates anxiety |
| **Subtle fade-in on scroll** | Acceptable via Intersection Observer — no animation library needed |
| **Hover transitions** | Quick (`duration-150` or `duration-200`), subtle color shifts |

---

## 6. Layout & Flow

### Landing Page Section Order

```
Hero → How It Works → Features → Providers → CTA Section → Footer
```

The flow from **LANDING_PAGE_DESIGN.md** is correct as designed. No reordering needed.

### Responsive Breakpoints

| Range | Label |
|-------|-------|
| 320px–767px | Mobile |
| 768px–1023px | Tablet |
| 1024px+ | Desktop |

### Key Responsive Rules

- Mobile-first CSS (base = mobile, `sm:`, `md:`, `lg:` to enhance)
- No horizontal scroll on any viewport
- Touch targets ≥ 44×44px on mobile
- Grids: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` pattern

---

## 7. DaisyUI Theme Configuration

Add this to `globals.css`:

```css
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
```

Apply with `data-theme="update-apply"` on the `<html>` tag.

---

## 8. Comparison: What We Avoid

| Style | Why It Doesn't Fit |
|-------|-------------------|
| **shadcn black-and-white** | Feels like a dev tool, not a career partner. Too sterile for something as personal as a job search. |
| **Supabase / Neon futuristic** | Exciting for builders, not reassuring for someone anxious about their career. Too cold. |
| **Overly playful (Retro, Cupcake, etc.)** | Undermines the seriousness of the mission. Job seeking is high-stakes. |
| **Corporate cold (strict blues, grays)** | Feels like a recruitment agency, not a supportive partner. No warmth. |

---

## 9. Quality Gates

Before shipping any themed UI:

- [ ] All colors match the palette above (no ad-hoc hex values)
- [ ] Typography uses the heading/body pairing (serif + sans)
- [ ] No emoji in the UI
- [ ] Icons are line-art SVGs, not filled illustrations
- [ ] All interactive elements meet WCAG AA contrast ratios
- [ ] Tested at 320px, 768px, and 1440px
- [ ] `prefers-reduced-motion` is respected
- [ ] No inline styles — everything uses daisyUI or Tailwind classes

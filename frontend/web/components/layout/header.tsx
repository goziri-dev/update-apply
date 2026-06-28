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

      {/* Right side — auth CTAs on desktop, hamburger on mobile */}
      <div className="navbar-end gap-2">
        {/* Desktop auth buttons */}
        <div className="hidden lg:flex items-center gap-2">
          <Link href="/sign-in" className="btn btn-ghost btn-sm">
            Sign In
          </Link>
          <Link href="/sign-up" className="btn btn-primary btn-sm">
            Get Started
          </Link>
        </div>

        {/* Mobile hamburger */}
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
      </div>
    </header>
  );
}

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

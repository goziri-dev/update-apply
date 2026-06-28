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

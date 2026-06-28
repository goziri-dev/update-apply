// components/landing/features.tsx
// Server Component.

const FEATURES = [
  {
    title: "Zero Data Entry",
    description:
      "Your profile builds itself from the work you have already done. Link your repos, and we surface your skills, projects, and experience. No tedious forms, no manual copying.",
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
      "Update your code or your docs, and your profile stays current everywhere. One sync keeps everything fresh across every platform you use.",
  },
  {
    title: "Smarter Over Time",
    description:
      "The more you use UpdateApply, the better it learns what makes you stand out. Every match improves. Every resume sharpens. Less friction, more momentum.",
  },
  {
    title: "Privacy First",
    description:
      "We read your files to understand your work. We never share them. You decide what gets connected, and you decide when to disconnect.",
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

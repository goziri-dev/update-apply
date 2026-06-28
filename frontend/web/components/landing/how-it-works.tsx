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
    description: "We match you to jobs that fit your stack and generate a tailored resume written specifically for that role. No templates. No guesswork.",
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

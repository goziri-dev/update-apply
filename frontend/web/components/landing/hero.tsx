// components/landing/hero.tsx
// Server Component.

import { GitHubIcon } from "@/components/providers/github-icon";
import { GoogleDriveIcon } from "@/components/providers/google-drive-icon";
import { NotionIcon } from "@/components/providers/notion-icon";

const PROVIDERS = [
  { name: "GitHub", Icon: GitHubIcon },
  { name: "Google Drive", Icon: GoogleDriveIcon },
  { name: "Notion", Icon: NotionIcon },
] as const;

export function Hero() {
  return (
    <section className="hero min-h-[90vh] md:min-h-[85vh] bg-base-200">
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
            Connect your repos, and we&apos;ll match you to jobs and tailor your resume. Automatically.
          </p>

          {/* Primary CTA */}
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <a href="/sign-up" className="btn btn-primary btn-lg text-base px-8">
              Get Started Free
            </a>
            <span className="text-sm text-base-content/60">No credit card required</span>
          </div>

          {/* Provider logos — brand trust signals */}
          <div className="mt-8 flex flex-wrap items-center justify-center lg:justify-start gap-x-6 gap-y-3 text-sm text-base-content/60">
            <span className="text-xs uppercase tracking-widest text-base-content/40">
              Syncs with
            </span>
            <div className="flex flex-wrap items-center gap-3">
              {PROVIDERS.map(({ name, Icon }) => (
                <span
                  key={name}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-neutral/60 text-base-content/70"
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span className="text-xs font-medium">{name}</span>
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

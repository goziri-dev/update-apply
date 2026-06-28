// components/landing/providers.tsx
// Server Component.

import { GitHubIcon } from "@/components/providers/github-icon";
import { GoogleDriveIcon } from "@/components/providers/google-drive-icon";
import { NotionIcon } from "@/components/providers/notion-icon";

const PROVIDERS = [
  {
    name: "GitHub",
    description: "Connect your repos, PRs, and contributions",
    Icon: GitHubIcon,
  },
  {
    name: "Google Drive",
    description: "Import your existing work and project documents",
    Icon: GoogleDriveIcon,
  },
  {
    name: "Notion",
    description: "Pull your career notes and project docs",
    Icon: NotionIcon,
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
                <div className="w-14 h-14 flex items-center justify-center mb-4">
                  <provider.Icon className="w-9 h-9" />
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

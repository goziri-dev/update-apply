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
      <body className="min-h-screen flex flex-col bg-base-200 text-base-content font-sans antialiased">
        {children}
      </body>
    </html>
  );
}

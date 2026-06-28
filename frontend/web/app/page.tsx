// app/page.tsx
// Server Component — composes all landing sections.

import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { Hero } from "@/components/landing/hero";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Features } from "@/components/landing/features";
import { Providers } from "@/components/landing/providers";
import { CtaSection } from "@/components/landing/cta-section";

export default function Home() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <HowItWorks />
        <Features />
        <Providers />
        <CtaSection />
      </main>
      <Footer />
    </>
  );
}

"use client";
import Hero from "@/components/landing/Hero";
import Navbar from "@/components/landing/Navbar";
import CTASection from "@/components/landing/CTASection"
import About from "@/components/landing/About"
import AgentsSection from "@/components/landing/AgentSection"; 
import ScrollJackSection from "@/components/landing/ScrollJackSection";
import Footer from "@/components/landing/Footer";


export default function LandingPage() {
  return (
    <main>
      <Navbar />
      <Hero />
      <CTASection />
      <About />
      <AgentsSection />
      <ScrollJackSection />
      <Footer />
    </main>
  );
}
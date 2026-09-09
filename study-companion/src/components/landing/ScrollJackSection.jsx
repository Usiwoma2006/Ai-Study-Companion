"use client";
import { useEffect, useRef, useState } from "react";
import { SCROLL_AGENTS } from "./ScrollData"; // adjust path to wherever you saved it

export default function ScrollJackSection() {
  const containerRef = useRef(null); // the tall 500vh outer div
  const [progress, setProgress] = useState(0); // 0 -> 1

  useEffect(() => {
    function handleScroll() {
      const el = containerRef.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      // rect.top: how far the container's top is from viewport top
      // rect.height: the full 500vh height
      // We want progress = 0 when container top just reaches viewport top,
      // and progress = 1 when container bottom reaches viewport top
      // (i.e. we've scrolled through the entire runway)

      const scrollable = rect.height - window.innerHeight;
      const scrolled = -rect.top; // becomes positive once top scrolls above 0

      let p = scrolled / scrollable;
      p = Math.min(1, Math.max(0, p)); // clamp between 0 and 1

      setProgress(p);
    }

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // run once on mount
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const translateX = -progress * 200; 

  return (
    <section ref={containerRef} style={{ height: "500vh" }} className="relative">
      <div className="sticky top-0 h-screen overflow-hidden bg-[#540B0E]">
        <div
          className="flex h-full"
          style={{ transform: `translateX(${translateX}vw)` }}
        >
          {SCROLL_AGENTS.map((agent) => (
            <div key={agent.id} className="w-[60vw] h-full flex-shrink-0 flex flex-col justify-center px-16">
              <span className="text-7xl font-bold text-[#E09F3E]">{agent.number}</span>
              <agent.icon className="w-10 h-10 text-[#E09F3E] mt-6" />
              <h2 className="text-6xl font-serif text-[#FFF3B0] mt-6">{agent.title}</h2>
              <p className="text-2xl text-[#FFF3B0]/90 mt-4">{agent.label}</p>
              <p className="text-base text-[#FFF3B0]/70 mt-6 max-w-2xl">{agent.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
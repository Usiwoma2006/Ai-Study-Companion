"use client";
import { useEffect, useRef, useState } from "react";
import { SCROLL_AGENTS } from "./ScrollData";

export default function ScrollJackSection() {
  const containerRef = useRef(null);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    function handleScroll() {
      const el = containerRef.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      const scrollable = rect.height - window.innerHeight;
      const scrolled = -rect.top;

      let p = scrolled / scrollable;
      p = Math.min(1, Math.max(0, p));

      setProgress(p);
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleScroll);
    handleScroll();
    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleScroll);
    };
  }, []);

  // Total panels = SCROLL_AGENTS.length; each panel is 100vw wide on mobile.
  // translateX moves the whole track left as you scroll.
  const translateX = -progress * 100 * (SCROLL_AGENTS.length - 1);

  return (
    <section
      ref={containerRef}
      style={{ height: `${SCROLL_AGENTS.length * 100}vh` }}
      className="relative"
    >
      <div className="sticky top-0 h-screen overflow-hidden bg-[#540B0E]">
        <div
          className="flex h-full"
          style={{ transform: `translateX(${translateX}vw)` }}
        >
          {SCROLL_AGENTS.map((agent) => (
            <div
              key={agent.id}
              className="w-screen h-full flex-shrink-0 flex flex-col justify-center
                         px-6 sm:px-10 md:px-16
                         max-w-full"
            >
              <span className="text-4xl sm:text-5xl md:text-7xl font-bold text-[#E09F3E]">
                {agent.number}
              </span>
              <agent.icon className="w-7 h-7 sm:w-9 sm:h-9 md:w-10 md:h-10 text-[#E09F3E] mt-4 md:mt-6" />
              <h2 className="text-2xl sm:text-4xl md:text-6xl font-serif text-[#FFF3B0] mt-4 md:mt-6 leading-tight">
                {agent.title}
              </h2>
              <p className="text-base sm:text-lg md:text-2xl text-[#FFF3B0]/90 mt-3 md:mt-4">
                {agent.label}
              </p>
              <p className="text-sm sm:text-base text-[#FFF3B0]/70 mt-4 md:mt-6 max-w-xl md:max-w-2xl">
                {agent.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
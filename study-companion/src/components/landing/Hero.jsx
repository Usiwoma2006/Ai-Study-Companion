import { useEffect, useRef, useState } from "react";

const palette = ["#335C67", "#E09F3E", "#9E2A2B", "#540B0E", "#335C67"];

function AnsweringHeadline() {
  const headlineRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => {
      setLoaded(true);
    });
  }, []);

  useEffect(() => {
    let rafId = null;

    const measure = () => {
      const el = headlineRef.current;
      if (!el) return;

      const rect = el.getBoundingClientRect();
      const raw =
        (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      const clamped = Math.min(1, Math.max(0, raw));

      setProgress(clamped);
    };

    const handleScroll = () => {
      if (rafId) return;
      rafId = requestAnimationFrame(() => {
        measure();
        rafId = null;
      });
    };

    measure();
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafId) cancelAnimationFrame(rafId);
    };
  }, []);

  const text = "Your notes, finally\nanswering\nback.";

  // Split into lines first (on \n), then each line into words,
  // keeping a running letter index so stagger/color stay continuous
  // across the whole headline, not reset per line/word.
  let letterCounter = 0;
  const lines = text.split("\n").map((line) => line.split(" "));

  return (
    <section>
      <h1
        ref={headlineRef}
        className="font-serif italic font-normal text-7xl sm:text-8xl md:text-9xl lg:text-[10rem] leading-none"
      >
        {lines.map((words, lineIndex) => (
          <div key={lineIndex}>
            {words.map((word, wordIndex) => (
              <span key={wordIndex}>
                <span className="inline-block" style={{ whiteSpace: "nowrap" }}>
                  {word.split("").map((char) => {
                    const i = letterCounter++;
                    const colorIndex =
                      (i + Math.floor(progress * palette.length)) % palette.length;
                    const color = palette[colorIndex];

                    return (
                      <span
                        key={i}
                        className="inline-block"
                        style={{
                          color,
                          opacity: loaded ? 1 : 0,
                          transform: loaded ? "translateY(0)" : "translateY(40px)",
                          transition:
                            "opacity 700ms ease, transform 700ms cubic-bezier(0.22, 1, 0.36, 1)",
                          transitionDelay: `${i * 25}ms`,
                        }}
                      >
                        {char}
                      </span>
                    );
                  })}
                </span>
                {wordIndex < words.length - 1 ? " " : ""}
              </span>
            ))}
          </div>
        ))}
      </h1>
    </section>
  );
}

export default AnsweringHeadline;
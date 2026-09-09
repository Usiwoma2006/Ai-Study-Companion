import { useEffect, useState } from "react";

const cards = [
  { key: "quiz", title: "Quiz", bg: "bg-[#E09F3E]" },
  { key: "plan", title: "Study Plan", bg: "bg-[#335C67]/65" },
  { key: "tutor", title: "Tutor", bg: "bg-[#9E2A2B]/70" },
];

function RecommendationCarousel() {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % cards.length);
    }, 3000);

    return () => clearInterval(id);
  }, []);

  return (
    <section>
      <h1 className="font-bold font-serif text-2xl text-oxblood pt-8 pb-6">
        Recommended for you
      </h1>

        <div className="relative h-[180px] flex items-center justify-center overflow-hidden">
        {cards.map((card, i) => {
            const rawOffset = i - activeIndex;

            const offset =
            ((rawOffset % cards.length) + cards.length) %
            cards.length;

            const position =
            offset === 0
                ? "translate-x-0 scale-110 opacity-100"
                : offset === 1
                ? "translate-x-[350px] scale-90 opacity-50"
                : "-translate-x-[350px] scale-90 opacity-50";

            return (
            <article
                key={card.key}
                className={`
                absolute
                rounded-xl p-6
                w-[200px] h-[140px]
                flex items-center justify-center
                transition-all duration-500
                ${card.bg}
                ${position}
                `}
            >
                <h2 className="font-bold font-serif text-xl text-oxblood">
                {card.title}
                </h2>
            </article>
            );
        })}
        </div>
    </section>
  );
}

export default RecommendationCarousel;
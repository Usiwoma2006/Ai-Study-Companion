import React from "react";

function AgentDetailBox({ activeAgent }) {
  if (!activeAgent) return null;

  const Icon = activeAgent.icon;

  return (
    <div className="w-full max-w-[467px] min-h-[240px] sm:min-h-[282px]
                    bg-[#FFFDF5] border border-[#540B0E]
                    px-6 py-6 sm:px-8 sm:py-8 md:px-10 md:py-10">

      {/* Icon */}
      <div className="mb-5 sm:mb-7 text-[#9E2A2B]">
        <Icon className="w-6 h-6 sm:w-7 sm:h-7" strokeWidth={1.5} />
      </div>

      {/* Category */}
      <span className="block text-[10px] sm:text-[11px] tracking-[0.3em] uppercase
                       text-[#335C67] mb-2 sm:mb-3">
        {activeAgent.category}
      </span>

      {/* Title */}
      <h3 className="font-serif font-bold text-2xl sm:text-3xl md:text-4xl
                     text-[#540B0E] mb-3 sm:mb-4">
        {activeAgent.title}
      </h3>

      {/* Description */}
      <p className="text-base sm:text-lg md:text-xl leading-relaxed text-[#9E2A2B]">
        {activeAgent.description}
      </p>
    </div>
  );
}

export default AgentDetailBox;
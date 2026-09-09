import React from "react";

function AgentDetailBox({ activeAgent }) {
    if (!activeAgent) return null;

    const Icon = activeAgent.icon;

    return (
        <div className="w-full max-w-[467px] min-h-[282px] bg-[#FFFDF5] border border-[#540B0E] px-10 py-10">

            {/* Icon */}
            <div className="mb-7 text-[#9E2A2B]">
                <Icon size={28} strokeWidth={1.5} />
            </div>

            {/* Category */}
            <span className="block text-[11px] tracking-[0.3em] uppercase text-[#335C67] mb-3">
                {activeAgent.category}
            </span>

            {/* Title */}
            <h3 className="font-serif font-bold text-4xl text-[#540B0E] mb-4">
                {activeAgent.title}
            </h3>

            {/* Description */}
            <p className="text-xl leading-relaxed text-[#9E2A2B]">
                {activeAgent.description}
            </p>
        </div>
    );
}

export default AgentDetailBox;
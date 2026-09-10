"use client";

import { useState, useRef } from "react";
import { AGENTS } from "./AgentData";
import AgentOrbit from "./AgentOrbit";
import AgentDetailBox from "./AgentDetailBox";

function AgentsSection() {
  const [activeAgent, setActiveAgent] = useState(AGENTS[0]);
  const detailRef = useRef(null);

  const handleSelect = (agent) => {
    setActiveAgent(agent);
    detailRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  return (
    <section className="min-h-screen bg-[#FFF4B5] px-4 sm:px-6 pt-12 sm:pt-16 pb-20 sm:pb-32">
      {/* Heading */}
      <div className="max-w-[650px] mx-auto md:mx-0 md:ml-[6%] text-center md:text-left">
        <h2 className="font-serif font-bold text-3xl sm:text-4xl md:text-5xl lg:text-6xl
                       leading-[1.15] text-[#540B0E]">
          Five agents, one student
          <br />
          in the middle.
        </h2>

        <p className="mt-4 sm:mt-5 text-xs sm:text-sm text-[#335C67]">
          Tap an agent to read what it does.
        </p>
      </div>

      {/* Orbit */}
      <div className="mt-10 sm:mt-12 md:mt-16">
        <AgentOrbit
          agents={AGENTS}
          activeAgent={activeAgent}
          onSelect={handleSelect}
        />
      </div>

      {/* Detail card */}
      <div ref={detailRef} className="mt-12 sm:mt-16 md:mt-20 flex justify-center">
        <AgentDetailBox activeAgent={activeAgent} />
      </div>
    </section>
  );
}

export default AgentsSection;
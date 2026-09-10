import React from 'react';

// Positions expressed as % of the container (0–100)
// so the orbit scales fluidly with the container size.
const POSITIONS = [
    { x: 50, y: 15 },  // top
    { x: 85, y: 32.5 }, // upper-right
    { x: 72.5, y: 72.5 }, // lower-right
    { x: 27.5, y: 72.5 }, // lower-left
    { x: 15, y: 32.5 },  // upper-left
];

function AgentOrbit({ agents, activeAgent, onSelect }) {
    return (
        <div className="relative w-full max-w-[560px] aspect-square mx-auto">
            {/* Outer ring */}
            <div className="absolute inset-0 z-0 flex items-center justify-center">
                <div className="w-[75%] h-[75%] rounded-full border-2 border-[#335C67]/20"></div>
            </div>

            {/* YOU circle */}
            <div className="absolute inset-0 z-10 flex items-center justify-center">
                <div
                    className="rounded-full bg-[#335C67] flex items-center justify-center
                               border-2 border-[#335C67] shadow-lg shadow-teal/20
                               w-[18%] h-[18%] min-w-[64px] min-h-[64px] max-w-[144px] max-h-[144px]"
                >
                    <span className="font-serif text-xs sm:text-sm md:text-base tracking-widest text-white">
                        YOU
                    </span>
                </div>
            </div>

            {agents.map((agent, index) => {
                const isActive = activeAgent?.id === agent.id;
                const Icon = agent.icon;
                const pos = POSITIONS[index] || { x: 50, y: 50 };

                return (
                    <div
                        key={agent.id}
                        className="absolute z-10 cursor-pointer group"
                        style={{
                            left: `${pos.x}%`,
                            top: `${pos.y}%`,
                            transform: 'translate(-50%, -50%)',
                        }}
                        onClick={() => onSelect(agent)}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                                e.preventDefault();
                                onSelect(agent);
                            }
                        }}
                    >
                        <div
                            className={`
                                rounded-xl flex items-center justify-center
                                border-2 transition-all duration-300 ease-in-out
                                w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20
                                ${isActive
                                    ? 'bg-[#335C67] text-white border-[#335C67] shadow-lg scale-110'
                                    : 'bg-white text-[#E09F3E] border-[#335C67]/20 hover:bg-[#335C67] hover:text-white hover:border-[#335C67]'
                                }
                            `}
                        >
                            <Icon className="w-5 h-5 sm:w-7 sm:h-7 md:w-8 md:h-8" strokeWidth={1.5} />
                        </div>

                        <div className="mt-2 text-center min-w-[64px] sm:min-w-[80px] md:min-w-[100px]">
                            <span
                                className={`
                                    text-[10px] sm:text-xs tracking-wider font-medium uppercase transition-colors duration-200
                                    ${isActive ? 'text-[#540B0E]' : 'text-[#335C67]/70 group-hover:text-[#540B0E]'}
                                `}
                            >
                                {agent.label}
                            </span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

export default AgentOrbit;
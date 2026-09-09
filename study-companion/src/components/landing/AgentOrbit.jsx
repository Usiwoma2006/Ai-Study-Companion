import React from 'react';

function AgentOrbit({ agents, activeAgent, onSelect }) {
    const positions = [
        { x: 280, y: 84 },
        { x: 476, y: 182 },
        { x: 406, y: 406 },
        { x: 154, y: 406 },
        { x: 84, y: 182 },
    ];

    return (
        <div className="relative w-[560px] h-[560px] mx-auto">
            <div className="absolute inset-0 z-0 flex items-center justify-center">
                <div className="w-[420px] h-[420px] rounded-full border-2 border-[#335C67]/20"></div>
            </div>

            {/* YOU circle — now bigger than the agent nodes, teal fill */}
            <div className="absolute inset-0 z-10 flex items-center justify-center">
                <div className="w-36 h-36 rounded-full bg-[#335C67] flex items-center justify-center
                                 border-2 border-[#335C67] shadow-lg shadow-teal/20">
                    <span className="font-serif text-base tracking-widest text-white">
                        YOU
                    </span>
                </div>
            </div>

            {agents.map((agent, index) => {
                const isActive = activeAgent?.id === agent.id;
                const Icon = agent.icon;
                const pos = positions[index] || { x: 280, y: 280 };

                return (
                    <div
                        key={agent.id}
                        className="absolute z-10 cursor-pointer group"
                        style={{
                            left: `${pos.x}px`,
                            top: `${pos.y}px`,
                            transform: 'translate(-50%, -50%)'
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
                        {/* Icon square — white box, orange icon, teal on hover/active */}
                        <div
                            className={`
                                w-20 h-20 rounded-xl flex items-center justify-center
                                border-2 transition-all duration-300 ease-in-out
                                ${isActive
                                    ? 'bg-[#335C67] text-white border-[#335C67] shadow-lg scale-110'
                                    : 'bg-white text-[#E09F3E] border-[#335C67]/20 hover:bg-[#335C67] hover:text-white hover:border-[#335C67]'
                                }
                            `}
                        >
                            <Icon size={32} strokeWidth={1.5} />
                        </div>

                        <div className="mt-2 text-center min-w-[100px]">
                            <span className={`
                                text-xs tracking-wider font-medium uppercase transition-colors duration-200
                                ${isActive ? 'text-[#540B0E]' : 'text-[#335C67]/70 group-hover:text-[#540B0E]'}
                            `}>
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
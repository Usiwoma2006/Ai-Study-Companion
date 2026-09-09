"use client";
import { Lightbulb, Calendar, CheckSquare, Telescope, TrendingUp } from "lucide-react";

const tools = [
  { id: "explain", label: "Explain It", icon: Lightbulb },
  { id: "plan", label: "Plan Study", icon: Calendar },
  { id: "test", label: "Test me", icon: CheckSquare },
  { id: "research", label: "Go deeper", icon: Telescope },
  { id: "progress", label: "My Progress", icon: TrendingUp },
];

export default function ToolsPanel({ activeId, onSelect }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {tools.map(({ id, label, icon: Icon }) => {
        const isActive = id === activeId;
        return (
          <button
            key={id}
            type="button"
            onClick={() => onSelect(id)}
            className={`w-full px-6 py-6 text-md font-medium flex-col items-center justify-center gap-2 ${
              isActive
                ? "bg-orange text-cream"
                : "bg-cream text-oxblood border border-oxblood/20"
            } ${id === "progress" ? "col-span-2" : ""}`}
          >
            <Icon size={16} aria-hidden="true" className="text-teal mb-2" />
            {label}
          </button>
        );
      })}
    </div>
  );
}
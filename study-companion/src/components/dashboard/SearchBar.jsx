"use client";
import { Search, Plus } from "lucide-react";

export default function SearchBar({ onCreateNew }) {
  return (
    <div className="flex gap-3 items-center mb-6">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-oxblood/50" />
        <input
          type="text"
          placeholder="Search your notebooks"
          className="w-full pl-9 pr-3 py-3 rounded-lg border border-teal/30 bg-white focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent text-sm"
        />
      </div>

      <button
        onClick={onCreateNew || (() => {})}
        className="flex items-center gap-2 px-4 py-3 rounded-lg bg-orange text-oxblood hover:bg-orange/80 transition-colors font-ui text-sm font-medium"
      >
        <Plus className="w-4 h-4" />
        Create new
      </button>
    </div>
  );
}
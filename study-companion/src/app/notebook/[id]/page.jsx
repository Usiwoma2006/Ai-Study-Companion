"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Plus, Settings, Menu, LayoutDashboard } from "lucide-react";
import Link from "next/link";
import ToolsPanel from "@/components/workspace/ToolsPanel";
import ToolOutputCard from "@/components/workspace/ToolOutputCard";
import SourcesPanel from "@/components/workspace/SourcesPanel";
import ChatPanel from "@/components/workspace/ChatPanel";
import api from "@/lib/api";

export default function NotebookWorkspace() {
  const { id } = useParams();
  const notebookId = Array.isArray(id) ? id[0] : id;

  const [activeId, setActiveId] = useState("progress");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [notebook, setNotebook] = useState(null);
  const [activeSourceId, setActiveSourceId] = useState(null);
  // Which panel shows in <main> below the lg breakpoint, where
  // Chat and Tools can't both fit on screen at once.
  const [mobileView, setMobileView] = useState("chat");

  useEffect(() => {
    if (!notebookId) return;
    api.get(`/${notebookId}/`).then(({ data }) => setNotebook(data));
  }, [notebookId]);

  return (
    <div className="h-screen flex flex-col bg-cream">
      <header className="flex items-center justify-between px-4 sm:px-6 py-4 bg-teal text-cream">
        <div className="flex items-center gap-3">
          <button className="lg:hidden" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <Menu size={20} />
          </button>
          <h1 className="font-display text-lg sm:text-xl">
            {notebook?.name || "Loading…"}
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/dashboard" aria-label="Back to dashboard">
            <LayoutDashboard size={20} />
          </Link>
          <Settings size={20} />
        </div>
      </header>

      {/* Chat / Tools tab-switcher — only shown below lg, where the
          Tools aside is hidden and would otherwise be unreachable */}
      <div className="lg:hidden flex border-b border-oxblood/10 bg-white">
        <button
          type="button"
          onClick={() => setMobileView("chat")}
          className={`flex-1 py-3 text-sm font-ui tracking-wide text-center ${
            mobileView === "chat"
              ? "text-teal border-b-2 border-orange"
              : "text-oxblood/50"
          }`}
        >
          CHAT
        </button>
        <button
          type="button"
          onClick={() => setMobileView("tools")}
          className={`flex-1 py-3 text-sm font-ui tracking-wide text-center ${
            mobileView === "tools"
              ? "text-teal border-b-2 border-orange"
              : "text-oxblood/50"
          }`}
        >
          TOOLS
        </button>
      </div>

      <div className="flex flex-1 min-h-0 relative">
        <aside className={`
          w-64 sm:w-72 
          border-r border-oxblood/10 
          p-4 overflow-y-auto bg-white
          fixed lg:relative inset-y-0 left-0 z-20
          transform transition-transform duration-300
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          lg:translate-x-0
        `}>
          <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
            <p className="font-ui text-md tracking-wide text-teal mb-4 pt-6 pb-4">SOURCES</p>
          </div>
          <SourcesPanel notebookId={notebookId} />
        </aside>

        {sidebarOpen && (
          <div className="fixed inset-0 bg-black/20 z-10 lg:hidden" onClick={() => setSidebarOpen(false)} />
        )}

        <main
          className={`
            flex-1 flex-col p-4 sm:p-6 overflow-hidden min-w-0
            ${mobileView === "tools" ? "hidden lg:flex" : "flex"}
          `}
        >
          {/* Removed overflow-y-auto wrapper - Chat now manages its own scrolling */}
          <ChatPanel notebookId={notebookId} />
        </main>

        {/* Mobile/tablet Tools view — reuses the same panel + output card
            as the desktop aside below, just rendered in <main> instead */}
        {mobileView === "tools" && (
          <main className="flex flex-1 flex-col p-4 sm:p-6 overflow-y-auto min-w-0 lg:hidden">
            <ToolsPanel activeId={activeId} onSelect={setActiveId} />
            <ToolOutputCard activeId={activeId} notebookId={notebookId} />
          </main>
        )}

        <aside className="
          w-64 sm:w-72 lg:w-80 
          border-l border-oxblood/10 
          p-4 overflow-y-auto bg-white
          hidden lg:block
        ">
          <p className="font-ui text-md tracking-wide text-teal mb-4 pt-6 pb-4">TOOLS</p>
          <ToolsPanel activeId={activeId} onSelect={setActiveId} />
          <ToolOutputCard activeId={activeId} notebookId={notebookId} />
        </aside>
      </div>
    </div>
  );
}
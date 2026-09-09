"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";
import api from "@/lib/api";

const badgeColors = ["bg-oxblood", "bg-teal", "bg-orange"];

function getBadgeColor(id) {
  const str = String(id);
  let sum = 0;
  for (let i = 0; i < str.length; i++) {
    sum += str.charCodeAt(i);
  }
  return badgeColors[sum % badgeColors.length];
}

function timeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) {
    return "just now";
  }
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return `${minutes} minute${minutes === 1 ? "" : "s"} ago`;
  }
  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  }
  const days = Math.floor(hours / 24);
  if (days === 1) {
    return "yesterday";
  }
  return `${days} days ago`;
}

export function CreateNotebookCard() {
  const router = useRouter();

  const [creating, setCreating] = useState(false);
  const [title, setTitle] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleCreate = async () => {
    if (!title.trim()) return;

    setSubmitting(true);

    try {
      const response = await api.post("/notebooks/", {
        name: title.trim(),
      });

      router.push(`/notebook/${response.data.id}`);
    } catch (error) {
      console.error("Failed to create notebook:", error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="border-2 border-dashed border-oxblood/30 bg-cream/60 rounded-xl p-6 flex items-center justify-center min-h-[180px]">
      {!creating ? (
        <button
          type="button"
          onClick={() => setCreating(true)}
          className="flex flex-col items-center gap-2 text-oxblood font-ui"
        >
          <Plus size={24} className="text-oxblood" />
          <span className="font-display text-lg">Create new</span>
        </button>
      ) : (
        <div className="flex flex-col gap-3 w-full">
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleCreate();
              }
            }}
            placeholder="Notebook name..."
            className="border border-oxblood/30 rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal"
            disabled={submitting}
            autoFocus
          />

          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleCreate}
              disabled={submitting || !title.trim()}
              className="flex-1 rounded-lg px-4 py-2 bg-orange text-oxblood font-ui text-sm font-medium disabled:opacity-50"
            >
              {submitting ? "Creating..." : "Create"}
            </button>

            <button
              type="button"
              onClick={() => {
                setCreating(false);
                setTitle("");
              }}
              disabled={submitting}
              className="rounded-lg px-4 py-2 border border-oxblood/20 text-oxblood font-ui text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export function NotebookCard({ notebook }) {
  notebook = notebook || { id: "1", name: "Sample Notebook", updated_at: new Date() };

  const initial = notebook.name?.charAt(0).toUpperCase() || "?";

  return (
    <Link
      href={`/notebook/${notebook.id}`}
      className="bg-white/60 rounded-xl p-6 flex flex-col gap-3 min-h-[180px] hover:bg-white/80 transition"
    >
      <div
        className={`w-10 h-10 rounded flex items-center justify-center font-bold text-cream ${getBadgeColor(
          notebook.id
        )}`}
      >
        {initial}
      </div>

      <span className="font-bold font-serif text-xl text-oxblood mt-auto">
        {notebook.name}
      </span>

      <p className="text-sm text-teal">{timeAgo(notebook.updated_at)}</p>
    </Link>
  );
}
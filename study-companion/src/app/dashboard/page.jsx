"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import Greetings from "@/components/dashboard/Greeting";
import SearchBar from "@/components/dashboard/SearchBar";
import RecommendationCarousel from "@/components/dashboard/RecommendationCarousel";
import { NotebookCard } from "@/components/dashboard/NotebookCard";
import { CreateNotebookCard } from "@/components/dashboard/NotebookCard";


export default function DashboardPage() {
  const [notebooks, setNotebooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadNotebooks = async () => {
      try {
        const response = await api.get("/notebooks");
        setNotebooks(response.data);
      } catch (error) {
        console.error("Failed to load notebooks:", error);
      } finally {
        setLoading(false);
      }
    };

    loadNotebooks();
  }, []);

  return (
    <div className="min-h-screen bg-cream px-4 sm:px-8 py-8 max-w-5xl mx-auto">
      <Greetings />

      <div className="mt-6">
        <SearchBar />
      </div>

      {<RecommendationCarousel /> }

      <div className="mt-10">
        <h2 className="font-bold font-serif italics text-2xl text-oxblood pt-8 pb-6">
          My Notebooks
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="min-h-[180px] rounded-xl bg-white/40 animate-pulse"
              />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {notebooks.map((notebook) => (
              <NotebookCard key={notebook.id} notebook={notebook} />
            ))}
            <CreateNotebookCard />
          </div>
        )}
      </div>
    </div>
  );
}
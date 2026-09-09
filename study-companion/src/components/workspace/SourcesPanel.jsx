"use client";
import { useState, useEffect, useCallback, useRef } from "react";
import { FileText, Upload, X, Loader2, AlertCircle } from "lucide-react";
import { listDocuments, uploadDocument, deleteDocument } from "@/lib/documents";

export default function SourcesPanel({ notebookId, activeSourceId, onSelectSource }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const fetchDocuments = useCallback(async () => {
    try {
      const docs = await listDocuments(notebookId);
      setDocuments(docs);
    } catch (err) {
      setError("Failed to load sources");
    } finally {
      setLoading(false);
    }
  }, [notebookId]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    try {
      const doc = await uploadDocument(notebookId, file);
      setDocuments((prev) => [doc, ...prev]);
    } catch (err) {
      setError("Upload failed. Try a smaller file or check the format.");
    } finally {
      setUploading(false);
      e.target.value = ""; // allow re-uploading the same filename
    }
  };

  const handleDelete = async (documentId, e) => {
    e.stopPropagation();
    try {
      await deleteDocument(notebookId, documentId);
      setDocuments((prev) => prev.filter((d) => d.id !== documentId));
    } catch (err) {
      setError("Delete failed");
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt"
        className="hidden"
        onChange={handleFileChange}
      />

      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        className="w-full px-6 py-4 text-sm font-medium flex items-center justify-center gap-2 bg-[#E09F3E] text-[#540B0E] border border-[#540B0E]/20 disabled:opacity-60"
      >
        {uploading ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            Uploading…
          </>
        ) : (
          <>
            <Upload size={16} />
            Add source
          </>
        )}
      </button>

      {error && (
        <div className="flex items-center gap-2 text-xs text-[#9E2A2B] px-2">
          <AlertCircle size={14} />
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-sm text-[#540B0E]/60 px-2">Loading sources…</div>
      ) : documents.length === 0 ? (
        <div className="text-sm text-[#540B0E]/60 px-2">No sources yet. Add one to get started.</div>
      ) : (
        documents.map((doc) => (
          <div
            key={doc.id}
            onClick={() => onSelectSource(doc.id)}
            className={`w-full px-6 py-4 text-sm font-medium flex items-center gap-2 border group cursor-pointer ${
              activeSourceId === doc.id
                ? "bg-[#FFF3B0] border-[#E09F3E]"
                : "bg-white border-[#540B0E]/20"
            }`}
          >
            ...
            <FileText size={16} aria-hidden="true" className="text-[#9E2A2B] flex-shrink-0" />
            <span className="break-words flex-1 min-w-0">{doc.title}</span>

            {doc.status === "failed" && (
              <span className="text-xs text-[#9E2A2B] flex-shrink-0">Failed</span>
            )}

            <button
              onClick={(e) => handleDelete(doc.id, e)}
              className="opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0 text-[#540B0E]/40 hover:text-[#9E2A2B]"
              aria-label={`Remove ${doc.title}`}
            >
              <X size={14} />
            </button>
          </div>
        ))
      )}
    </div>
  );
}
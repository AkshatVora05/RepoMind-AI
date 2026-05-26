"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getRepository, deleteRepository } from "../../services/api";
import { RepoResponse } from "../../types";
import { ArchitectureCard } from "../../components/ArchitectureCard";
import { ChatBox } from "../../components/ChatBox";
import { LoadingSpinner } from "../../components/LoadingSpinner";
import { ArrowLeft, Trash2, GitBranch } from "lucide-react";

function AnalyzeContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const id = searchParams.get("id");
  
  const [repo, setRepo] = useState<RepoResponse | null>(null);
  const [error, setError] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    if (!id) {
      router.push("/");
      return;
    }

    let interval: NodeJS.Timeout;
    const fetchRepo = async () => {
      try {
        const data = await getRepository(id);
        setRepo(data);
        
        // If still processing, poll every 3 seconds
        if (data.status === "PROCESSING" || data.status === "PENDING") {
          interval = setTimeout(fetchRepo, 5000);
        }
      } catch (err) {
        setError("Repository not found or error fetching details.");
      }
    };

    fetchRepo();

    return () => clearTimeout(interval);
  }, [id, router]);

  const handleDelete = () => {
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    if (!id) return;
    setIsDeleting(true);
    try {
      await deleteRepository(id);
      router.push("/");
    } catch (err) {
      alert("Failed to delete repository.");
      setIsDeleting(false);
      setShowDeleteModal(false);
    }
  };

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <p className="text-red-500 mb-4">{error}</p>
        <button onClick={() => router.push("/")} className="text-blue-600 hover:underline">Go Back</button>
      </div>
    );
  }

  if (!repo) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner text="Connecting to RepoMind Engine..." />
      </div>
    );
  }

  return (
    <>
      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full mx-4 shadow-xl border border-slate-200 animate-in zoom-in-95 duration-200">
            <div className="flex items-center space-x-3 text-red-600 mb-4">
              <div className="p-3 bg-red-100 rounded-full">
                <Trash2 className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-800">Delete Repository?</h3>
            </div>
            <p className="text-slate-600 mb-6">
              Are you sure you want to completely remove <span className="font-semibold text-slate-800">{repo.id}</span> from the intelligence engine? This action cannot be undone.
            </p>
            <div className="flex space-x-3 justify-end">
              <button 
                onClick={() => setShowDeleteModal(false)}
                disabled={isDeleting}
                className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg font-medium transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={confirmDelete}
                disabled={isDeleting}
                className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
              >
                {isDeleting ? "Deleting..." : "Yes, Delete"}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
      
        {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex items-center space-x-4">
          <button onClick={() => router.push("/")} className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center space-x-2 text-slate-800">
              <GitBranch className="w-5 h-5" />
              <h1 className="text-xl font-bold">{repo.id}</h1>
            </div>
            <p className="text-sm text-slate-500 mt-1">
              Status: <span className="font-medium text-blue-600">{repo.status}</span>
            </p>
          </div>
        </div>
        
        <button 
          onClick={handleDelete}
          disabled={isDeleting}
          className="flex items-center justify-center space-x-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg border border-red-100 hover:bg-red-100 hover:border-red-200 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
          <span className="text-sm font-medium">Delete Repository</span>
        </button>
      </div>

      {/* Main Content Grid */}
      {repo.status === "COMPLETED" ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <ArchitectureCard summary={repo.architecture_summary || ""} />
          </div>
          <div>
            <ChatBox repoId={repo.id} />
          </div>
        </div>
      ) : repo.status === "FAILED" ? (
        <div className="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center text-center">
          <div className="p-4 bg-red-100 rounded-full mb-4">
            <Trash2 className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-xl font-bold text-slate-800 mb-2">Ingestion Failed</h2>
          <p className="text-slate-500 max-w-md">
            The intelligence engine encountered an unexpected error while processing this repository. Please try deleting and re-ingesting it.
          </p>
        </div>
      ) : (
        <div className="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center min-h-[300px] justify-center">
          <LoadingSpinner />
        </div>
      )}

    </div>
    </>
  );
}

export default function AnalyzePage() {
  return (
    <main className="min-h-screen p-4 md:p-8">
      <Suspense fallback={<div className="flex justify-center p-20"><LoadingSpinner text="Loading Interface..." /></div>}>
        <AnalyzeContent />
      </Suspense>
    </main>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { RepoInput } from "../components/RepoInput";
import { ingestRepository } from "../services/api";
import { BrainCircuit } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleIngest = async (url: string) => {
    setIsLoading(true);
    setError("");
    try {
      const response = await ingestRepository(url);
      // Navigate to the analysis dashboard with the id
      router.push(`/analyze?id=${response.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to ingest repository. Please ensure it is a valid public GitHub URL.");
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-slate-50 to-slate-100">
      <div className="w-full max-w-4xl mx-auto flex flex-col items-center text-center space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">

        <div className="space-y-4">
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900">
            RepoMind <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">AI</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-500 max-w-2xl mx-auto">
            Ingest any public GitHub repository and uncover deep architectural insights using RepoMind AI.
          </p>
        </div>

        <div className="w-full pt-8">
          <RepoInput onSubmit={handleIngest} isLoading={isLoading} />
          {error && (
            <div className="mt-6 p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 text-sm animate-in fade-in">
              {error}
            </div>
          )}
          {isLoading && (
            <div className="mt-6 text-sm text-blue-600 animate-pulse font-medium">
              Initializing Engine...
            </div>
          )}
        </div>

      </div>
    </main>
  );
}

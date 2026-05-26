"use client";

import { useState } from "react";
import { ArrowRight, GitBranch } from "lucide-react";
import { cn } from "../utils/cn";

interface RepoInputProps {
  onSubmit: (url: string) => void;
  isLoading: boolean;
}

export const RepoInput = ({ onSubmit, isLoading }: RepoInputProps) => {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim() && !isLoading) {
      onSubmit(url.trim());
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form
        onSubmit={handleSubmit}
        className={cn(
          "relative flex items-center w-full transition-all duration-300",
          "bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.04)]",
          "border border-slate-100 hover:border-slate-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)]",
          "focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10 focus-within:shadow-[0_8px_30px_rgb(0,0,0,0.08)]"
        )}
      >
        <div className="pl-6 text-slate-400">
          <GitBranch className="w-5 h-5" />
        </div>
        
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/owner/repository"
          disabled={isLoading}
          className="w-full py-5 pl-4 pr-16 bg-transparent text-slate-800 placeholder-slate-400 focus:outline-none disabled:opacity-50 text-lg"
          required
        />
        
        <button
          type="submit"
          disabled={isLoading || !url}
          className={cn(
            "absolute right-3 p-3 rounded-xl flex items-center justify-center transition-all duration-300",
            isLoading || !url 
              ? "bg-slate-100 text-slate-400" 
              : "bg-slate-900 text-white hover:bg-slate-800 active:scale-95 shadow-md cursor-pointer"
          )}
        >
          <ArrowRight className="w-5 h-5" />
        </button>
      </form>
      <p className="text-center text-sm text-slate-400 mt-4">
        Enter any public GitHub repository URL to begin deep architectural analysis.
      </p>
    </div>
  );
};

"use client";

import ReactMarkdown from "react-markdown";
import { FileCode2 } from "lucide-react";

interface ArchitectureCardProps {
  summary: string;
}

export const ArchitectureCard = ({ summary }: ArchitectureCardProps) => {
  if (!summary) return null;

  return (
    <div className="w-full bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="bg-slate-50 border-b border-slate-100 px-6 py-4 flex items-center space-x-3">
        <FileCode2 className="w-5 h-5 text-blue-600" />
        <h2 className="text-lg font-semibold text-slate-800">Architectural Summary</h2>
      </div>
      
      <div className="p-6 prose prose-slate max-w-none prose-headings:font-semibold prose-a:text-blue-600">
        <ReactMarkdown>{summary}</ReactMarkdown>
      </div>
    </div>
  );
};

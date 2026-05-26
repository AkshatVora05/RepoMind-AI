"use client";

import { Citation } from "../types";
import { FileText } from "lucide-react";

export const RetrievedChunks = ({ citations }: { citations: Citation[] }) => {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="mt-4 space-y-3">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Sources Cited</h4>
      <div className="grid grid-cols-1 gap-2">
        {citations.map((c, idx) => (
          <div key={idx} className="bg-slate-50 rounded-lg p-3 border border-slate-200 text-sm group transition-colors hover:bg-slate-100 hover:border-slate-300">
            <div className="flex items-center space-x-2 text-slate-700 font-medium mb-2">
              <FileText className="w-4 h-4 text-blue-500" />
              <span className="truncate">{c.file_path}</span>
            </div>
            <pre className="text-xs bg-slate-200/50 p-2 rounded text-slate-600 overflow-x-auto font-mono">
              <code>{c.text_snippet}</code>
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};

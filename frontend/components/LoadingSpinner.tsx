import { Loader2 } from "lucide-react";
import { useState, useEffect } from "react";

const DEFAULT_QUOTES = [
  "Parsing Abstract Syntax Trees...",
  "Waking up the AI Engine...",
  "Generating multi-dimensional embeddings...",
  "Uploading vectors to Pinecone...",
  "Analyzing backend architecture...",
  "Brewing coffee while reading code...",
  "Extracting technical roadmap...",
  "Almost there, finalizing insights..."
];

interface LoadingSpinnerProps {
  text?: string;
  quotes?: string[];
}

export const LoadingSpinner = ({ text, quotes }: LoadingSpinnerProps) => {
  const [index, setIndex] = useState(0);
  
  const displayQuotes = quotes || DEFAULT_QUOTES;
  const isRotating = !text;

  useEffect(() => {
    if (!isRotating) return;
    
    const interval = setInterval(() => {
      setIndex((prev) => {
        if (prev >= displayQuotes.length - 1) {
          clearInterval(interval);
          return prev;
        }
        return prev + 1;
      });
    }, 3500);
    
    return () => clearInterval(interval);
  }, [isRotating, displayQuotes.length]);

  return (
    <div className="flex flex-col items-center justify-center space-y-4 py-10">
      <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
      <p className="text-sm font-medium text-slate-600 animate-pulse transition-opacity duration-500 text-center max-w-sm">
        {isRotating ? displayQuotes[index] : text}
      </p>
    </div>
  );
};

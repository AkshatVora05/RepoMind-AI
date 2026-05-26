import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "../utils/cn";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "RepoMind AI",
  description: "AI-powered repository intelligence and RAG.",
  icons: {
    icon: "/icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={cn(inter.className, "antialiased selection:bg-blue-100 selection:text-blue-900 bg-[#f8fafc] text-slate-900 min-h-screen flex flex-col")}>
        <div className="flex-1">
          {children}
        </div>
      </body>
    </html>
  );
}

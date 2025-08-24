"use client";

import { ReactNode } from "react";
import Sidebar from "./Sidebar";

interface MainLayoutProps {
  children: ReactNode;
  onLogout: () => void;
}

export default function MainLayout({ children, onLogout }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar onLogout={onLogout} />

      {/* Main content */}
      <div className="lg:pl-64">
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

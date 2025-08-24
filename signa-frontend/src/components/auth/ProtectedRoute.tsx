"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoading, isAuthenticated, isClient } = useAuth();
  const router = useRouter();
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    if (isClient && !isLoading) {
      if (!isAuthenticated()) {
        router.push("/");
      } else {
        setShouldRender(true);
      }
    }
  }, [isClient, isLoading, isAuthenticated, router]);

  // Mostrar loading mientras se verifica la autenticación
  if (!isClient || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  // No renderizar nada si no está autenticado
  if (!shouldRender) {
    return null;
  }

  return <>{children}</>;
}

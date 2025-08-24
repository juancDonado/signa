import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";

interface User {
  id: number;
  name: string;
  surname: string;
  email: string;
  username: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isClient, setIsClient] = useState(false);
  const router = useRouter();

  // Verificar si estamos en el cliente
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Verificar si el usuario está autenticado al cargar (solo en cliente)
  useEffect(() => {
    if (!isClient) return;

    const accessToken = localStorage.getItem("access_token");
    const userData = localStorage.getItem("user");

    if (accessToken && userData) {
      try {
        setToken(accessToken);
        setUser(JSON.parse(userData));
      } catch (error) {
        console.error("Error parsing user data:", error);
        logout();
      }
    }
    setIsLoading(false);
  }, [isClient]);

  // Función de login
  const login = useCallback(
    (accessToken: string, userData: User) => {
      if (!isClient) return;

      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("user", JSON.stringify(userData));
      setToken(accessToken);
      setUser(userData);
    },
    [isClient]
  );

  // Función de logout
  const logout = useCallback(() => {
    if (!isClient) return;

    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
    router.push("/");
  }, [router, isClient]);

  // Verificar si el usuario está autenticado
  const isAuthenticated = useCallback(() => {
    return !!token && !!user;
  }, [token, user]);

  // Obtener headers de autenticación
  const getAuthHeaders = useCallback((): HeadersInit => {
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }, [token]);

  return {
    user,
    token,
    isLoading: isLoading || !isClient,
    login,
    logout,
    isAuthenticated,
    getAuthHeaders,
    isClient,
  };
}

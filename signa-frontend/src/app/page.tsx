"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import LoginForm from "@/components/forms/LoginForm";

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("access_token");
    if (token) {
      router.push("/register-sign");
    }
  }, [router]);

  const handleLoginSuccess = (token: string) => {
    router.push("/register-sign");
  };

  return <LoginForm onLoginSuccess={handleLoginSuccess} />;
}

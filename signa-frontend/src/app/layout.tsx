import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Signa - Sistema de Gestión de Marcas",
  description:
    "Sistema moderno para la gestión y registro de marcas comerciales",
  keywords: "marcas, registro, gestión, comercio, signa",
  authors: [{ name: "Signa Team" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  );
}

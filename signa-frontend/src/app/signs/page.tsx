"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import MainLayout from "@/components/layout/MainLayout";
import EditSignModal from "@/components/modals/EditSignModal";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  DocumentTextIcon,
} from "@heroicons/react/24/outline";
import { SignWithUser } from "@/types";
import { apiService } from "@/services/api";
import { useAuth } from "@/hooks/useAuth";

export default function MisMarcasPage() {
  const router = useRouter();
  const { logout } = useAuth();
  const [signs, setSigns] = useState<SignWithUser[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedSign, setSelectedSign] = useState<SignWithUser | null>(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [signToDelete, setSignToDelete] = useState<SignWithUser | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/");
      return;
    }

    fetchSigns();
  }, [router]);

  const fetchSigns = async () => {
    try {
      setIsLoading(true);
      setError(""); // Limpiar errores previos
      const response = await apiService.getSigns();

      console.log("Respuesta de la API getSigns:", response);

      // La respuesta ya viene como SignWithUser[]
      if (Array.isArray(response)) {
        setSigns(response);
      } else {
        console.warn("Respuesta inesperada de la API:", response);
        setSigns([]);
      }
    } catch (err) {
      console.error("Error al cargar marcas:", err);
      setError(
        err instanceof Error ? err.message : "Error al cargar las marcas"
      );
      setSigns([]); // Establecer array vacío en caso de error
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const handleEdit = (sign: SignWithUser) => {
    setSelectedSign(sign);
    setIsEditModalOpen(true);
  };

  const handleDelete = (sign: SignWithUser) => {
    setSignToDelete(sign);
    setIsDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!signToDelete) return;

    setIsDeleting(true);
    try {
      await apiService.deleteSign(signToDelete.sign.id);
      setSuccess("Marca eliminada exitosamente");

      // Actualizar la lista
      setSigns((prev) =>
        prev.filter((s) => s.sign.id !== signToDelete.sign.id)
      );

      // Limpiar mensaje después de 3 segundos
      setTimeout(() => setSuccess(""), 3000);

      // Cerrar diálogo
      setIsDeleteDialogOpen(false);
      setSignToDelete(null);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al eliminar la marca"
      );

      // Limpiar mensaje después de 5 segundos
      setTimeout(() => setError(""), 5000);
    } finally {
      setIsDeleting(false);
    }
  };

  const cancelDelete = () => {
    setIsDeleteDialogOpen(false);
    setSignToDelete(null);
    setIsDeleting(false);
  };

  const handleUpdate = () => {
    fetchSigns(); // Recargar las marcas
  };

  if (isLoading) {
    return (
      <MainLayout onLogout={handleLogout}>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout onLogout={handleLogout}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Marcas</h1>
            <p className="text-gray-600 mt-1">
              Gestiona todas tus marcas registradas
            </p>
          </div>

          {Array.isArray(signs) && signs.length !== 0 && (
            <button
              onClick={() => router.push("/register-sign")}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Registrar Marca
            </button>
          )}
        </div>

        {/* Mensajes de error y éxito */}
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="rounded-md bg-green-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">
                  {success}
                </h3>
              </div>
            </div>
          </div>
        )}

        {/* Signs Grid */}
        {!Array.isArray(signs) || signs.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto h-12 w-12 text-gray-400">
              <DocumentTextIcon className="h-12 w-12" />
            </div>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No hay marcas
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {!Array.isArray(signs)
                ? "Error al cargar las marcas"
                : "Comienza registrando tu primera marca."}
            </p>
            <div className="mt-6">
              <button
                onClick={() => router.push("/register-sign")}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Registrar Marca
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {signs.map((signWithUser) => (
              <div
                key={signWithUser.sign.id}
                className="bg-white overflow-hidden shadow-sm rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      {signWithUser.sign.sign_name}
                    </h3>
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        signWithUser.sign.status
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {signWithUser.sign.status ? "Activa" : "Inactiva"}
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Titular:</span>{" "}
                      {signWithUser.user.name} {signWithUser.user.surname}
                    </p>
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Email:</span>{" "}
                      {signWithUser.user.email}
                    </p>
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Dirección:</span>{" "}
                      {signWithUser.user.address}
                    </p>
                  </div>

                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(signWithUser)}
                      className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <PencilIcon className="h-4 w-4 mr-1" />
                      Editar
                    </button>

                    <button
                      onClick={() => handleDelete(signWithUser)}
                      className="inline-flex items-center justify-center px-3 py-2 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal de Edición */}
      <EditSignModal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedSign(null);
        }}
        signData={selectedSign}
        onUpdate={handleUpdate}
      />

      {/* Diálogo de Confirmación de Eliminación */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onConfirm={confirmDelete}
        onClose={cancelDelete}
        isLoading={isDeleting}
        title="Eliminar Marca"
        message={`¿Estás seguro de que quieres eliminar la marca "${signToDelete?.sign.sign_name}"? Esta acción no se puede deshacer.`}
      />
    </MainLayout>
  );
}

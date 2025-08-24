"use client";

import { useState, useEffect } from "react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { SignWithUser, UpdateSignData } from "@/types";
import { apiService } from "@/services/api";

interface EditSignModalProps {
  isOpen: boolean;
  onClose: () => void;
  signData: SignWithUser | null;
  onUpdate: () => void;
}

export default function EditSignModal({
  isOpen,
  onClose,
  signData,
  onUpdate,
}: EditSignModalProps) {
  const [formData, setFormData] = useState<UpdateSignData>({
    sign_name: "",
    name: "",
    surname: "",
    email: "",
    address: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Actualizar formData cuando cambie signData
  useEffect(() => {
    if (signData) {
      setFormData({
        sign_name: signData.sign.sign_name || "",
        name: signData.user.name || "",
        surname: signData.user.surname || "",
        email: signData.user.email || "",
        address: signData.user.address || "",
      });
      // Limpiar mensajes previos
      setError("");
      setSuccess("");
    }
  }, [signData]);

  const handleInputChange = (field: keyof UpdateSignData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Limpiar errores cuando el usuario empiece a escribir
    if (error) setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!signData) return;

    setIsLoading(true);
    setError("");
    setSuccess("");

    try {
      // Solo enviar campos que han sido modificados
      const modifiedData: UpdateSignData = {};
      Object.keys(formData).forEach((key) => {
        const field = key as keyof UpdateSignData;
        const originalValue =
          field === "sign_name"
            ? signData.sign.sign_name
            : signData.user[field as keyof typeof signData.user];

        if (formData[field] !== originalValue) {
          modifiedData[field] = formData[field];
        }
      });

      // Si no hay cambios, mostrar mensaje y no hacer la petición
      if (Object.keys(modifiedData).length === 0) {
        setSuccess("No hay cambios para actualizar");
        setTimeout(() => {
          onClose();
          setSuccess("");
        }, 1500);
        return;
      }

      console.log("Datos a actualizar:", modifiedData);

      await apiService.updateSign(signData.sign.id, modifiedData);
      setSuccess("Marca actualizada exitosamente");

      // Cerrar modal después de 2 segundos
      setTimeout(() => {
        onUpdate();
        onClose();
        setSuccess("");
      }, 2000);
    } catch (err) {
      console.error("Error al actualizar marca:", err);
      setError(
        err instanceof Error ? err.message : "Error al actualizar la marca"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    if (!isLoading) {
      setError("");
      setSuccess("");
      onClose();
    }
  };

  // Prevenir cierre si está cargando
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && !isLoading) {
      handleClose();
    }
  };

  if (!isOpen || !signData) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black/20 transition-opacity"
          onClick={handleBackdropClick}
        />

        {/* Modal */}
        <div className="relative w-full max-w-2xl bg-white rounded-lg shadow-xl">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Editar Marca: {signData.sign.sign_name}
            </h3>
            <button
              onClick={handleClose}
              disabled={isLoading}
              className="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-4 space-y-4">
            {/* Mensajes de error y éxito */}
            {error && (
              <div className="rounded-md bg-red-50 p-3">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      {error}
                    </h3>
                  </div>
                </div>
              </div>
            )}

            {success && (
              <div className="rounded-md bg-green-50 p-3">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">
                      {success}
                    </h3>
                  </div>
                </div>
              </div>
            )}

            {/* Información de la Marca */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-3">
                Información de la Marca
              </h4>
              <div className="grid grid-cols-1 gap-3">
                <div>
                  <label
                    htmlFor="sign_name"
                    className="block text-sm font-medium text-gray-400 mb-2"
                  >
                    Nombre de la Marca *
                  </label>
                  <input
                    type="text"
                    id="sign_name"
                    value={formData.sign_name}
                    onChange={(e) =>
                      handleInputChange("sign_name", e.target.value)
                    }
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11 px-3 text-black placeholder-gray-500"
                    placeholder="Nombre de la marca"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Información del Titular */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-3">
                Información del Titular
              </h4>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                  <label
                    htmlFor="name"
                    className="block text-sm font-medium text-gray-400 mb-2"
                  >
                    Nombre *
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formData.name}
                    onChange={(e) => handleInputChange("name", e.target.value)}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11 px-3 text-black placeholder-gray-500"
                    placeholder="Nombre"
                    required
                  />
                </div>

                <div>
                  <label
                    htmlFor="surname"
                    className="block text-sm font-medium text-gray-400 mb-2"
                  >
                    Apellido *
                  </label>
                  <input
                    type="text"
                    id="surname"
                    value={formData.surname}
                    onChange={(e) =>
                      handleInputChange("surname", e.target.value)
                    }
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11 px-3 text-black placeholder-gray-500"
                    placeholder="Apellido"
                    required
                  />
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-400 mb-2"
                  >
                    Email *
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11 px-3 text-black placeholder-gray-500"
                    placeholder="email@ejemplo.com"
                    required
                  />
                </div>

                <div>
                  <label
                    htmlFor="address"
                    className="block text-sm font-medium text-gray-400 mb-2"
                  >
                    Dirección *
                  </label>
                  <input
                    type="text"
                    id="address"
                    value={formData.address}
                    onChange={(e) =>
                      handleInputChange("address", e.target.value)
                    }
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-11 px-3 text-black placeholder-gray-500"
                    placeholder="Dirección completa"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Estado de la Marca */}
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-3">
                Estado de la Marca
              </h4>
              <div className="flex items-center space-x-3">
                <span
                  className={`inline-flex items-center px-2.5 py-1 rounded-full text-sm font-medium ${
                    signData.sign.status
                      ? "bg-green-100 text-green-800"
                      : "bg-red-100 text-red-800"
                  }`}
                >
                  {signData.sign.status ? "Activa" : "Inactiva"}
                </span>
                <p className="text-sm text-gray-500">
                  El estado de la marca no se puede modificar desde este
                  formulario
                </p>
              </div>
            </div>

            {/* Botones de Acción */}
            <div className="flex justify-end space-x-3 pt-3 border-t border-gray-200">
              <button
                type="button"
                onClick={handleClose}
                disabled={isLoading}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-400 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? "Actualizando..." : "Actualizar Marca"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

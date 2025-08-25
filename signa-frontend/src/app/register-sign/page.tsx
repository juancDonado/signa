"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import MainLayout from "@/components/layout/MainLayout";
import Stepper from "@/components/ui/Stepper";
import { CreateSignData, Step } from "@/types";
import { apiService } from "@/services/api";
import { useAuth } from "@/hooks/useAuth";

export default function RegistroMarcaPage() {
  const router = useRouter();
  const { logout } = useAuth();
  const [currentStep, setCurrentStep] = useState<1 | 2 | 3>(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [formData, setFormData] = useState<CreateSignData>({
    sign_name: "",
    name: "",
    surname: "",
    email: "",
    address: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/");
    }
  }, [router]);

  const steps = [
    {
      id: 1 as Step,
      title: "Nombre de la Marca",
      description: "Información básica",
    },
    {
      id: 2 as Step,
      title: "Información del Titular",
      description: "Datos personales",
    },
    { id: 3 as Step, title: "Resumen", description: "Confirmar datos" },
  ];

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep((prev) => (prev + 1) as 1 | 2 | 3);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => (prev - 1) as 1 | 2 | 3);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const updateFormData = (field: keyof CreateSignData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError("");
    setSuccess("");

    try {
      await apiService.createSign(formData);
      setSuccess("Marca creada exitosamente");

      // Limpiar formulario
      setFormData({
        sign_name: "",
        name: "",
        surname: "",
        email: "",
        address: "",
      });

      // Redirigir a mis marcas después de 2 segundos
      setTimeout(() => {
        router.push("/signs");
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al crear la marca");
    } finally {
      setIsLoading(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                Nombre de la Marca
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                Ingresa el nombre de la marca que deseas registrar
              </p>
            </div>

            <div>
              <label
                htmlFor="sign_name"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Nombre de la Marca *
              </label>
              <input
                type="text"
                id="sign_name"
                value={formData.sign_name}
                onChange={(e) => updateFormData("sign_name", e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-12 px-4 text-black placeholder-gray-500"
                placeholder="Ej: Mi Marca Comercial"
                required
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                Información del Titular
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                Completa la información personal del titular de la marca
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Nombre *
                </label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={(e) => updateFormData("name", e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-12 px-4 text-black placeholder-gray-500"
                  placeholder="Nombre"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="surname"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Apellido *
                </label>
                <input
                  type="text"
                  id="surname"
                  value={formData.surname}
                  onChange={(e) => updateFormData("surname", e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-12 px-4 text-black placeholder-gray-500"
                  placeholder="Apellido"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Email *
                </label>
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) => updateFormData("email", e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-12 px-4 text-black placeholder-gray-500"
                  placeholder="email@ejemplo.com"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="address"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Dirección *
                </label>
                <input
                  type="text"
                  id="address"
                  value={formData.address}
                  onChange={(e) => updateFormData("address", e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm h-12 px-4 text-black placeholder-gray-500"
                  placeholder="Dirección completa"
                  required
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                Resumen de la Información
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                Revisa todos los datos antes de confirmar el registro
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6 space-y-4">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">
                  Información de la Marca
                </h4>
                <div className="bg-white rounded-md p-4">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Nombre:</span>{" "}
                    {formData.sign_name}
                  </p>
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-900 mb-2">
                  Información del Titular
                </h4>
                <div className="bg-white rounded-md p-4 space-y-2">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Nombre completo:</span>{" "}
                    {formData.name} {formData.surname}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Email:</span> {formData.email}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Dirección:</span>{" "}
                    {formData.address}
                  </p>
                </div>
              </div>
            </div>

            {/* Mensajes de error y éxito */}
            {error && (
              <div className="rounded-md bg-red-50 p-4">
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
          </div>
        );

      default:
        return null;
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return formData.sign_name.trim() !== "";
      case 2:
        return (
          formData.name.trim() !== "" &&
          formData.surname.trim() !== "" &&
          formData.email.trim() !== "" &&
          formData.address.trim() !== ""
        );
      case 3:
        return true;
      default:
        return false;
    }
  };

  return (
    <MainLayout onLogout={handleLogout}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          {/* <div className="bg-red-600 text-white px-4 py-2 rounded-t-lg inline-block">
            Servicios / Registro de Marca
          </div> */}
          <h1 className="text-2xl font-bold text-gray-900 mt-2">
            Registro de Marca
          </h1>
        </div>

        {/* Stepper */}
        <div className="mt-2 mb-9">
          <Stepper currentStep={currentStep} steps={steps} />
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm mt-8 p-8">
          {renderStepContent()}
        </div>

        {/* Navigation Buttons */}
        <div className="mt-8 flex justify-between">
          <button
            onClick={handleBack}
            disabled={currentStep === 1}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Atrás
          </button>

          {currentStep === 3 ? (
            <button
              onClick={handleSubmit}
              disabled={!canProceed() || isLoading}
              className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? "Creando Marca..." : "Confirmar Registro"}
            </button>
          ) : (
            <button
              onClick={handleNext}
              disabled={!canProceed()}
              className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Continuar →
            </button>
          )}
        </div>
      </div>
    </MainLayout>
  );
}

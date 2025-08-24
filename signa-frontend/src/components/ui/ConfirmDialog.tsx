"use client";

import { Fragment } from "react";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";

interface ConfirmDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  confirmButtonColor?: "red" | "blue" | "green" | "gray";
  isLoading?: boolean;
}

export default function ConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = "Confirmar",
  cancelText = "Cancelar",
  confirmButtonColor = "red",
  isLoading = false,
}: ConfirmDialogProps) {
  if (!isOpen) return null;

  const getConfirmButtonClasses = () => {
    const baseClasses =
      "px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors";

    switch (confirmButtonColor) {
      case "red":
        return `${baseClasses} bg-red-600 hover:bg-red-700 focus:ring-red-500`;
      case "blue":
        return `${baseClasses} bg-blue-600 hover:bg-blue-700 focus:ring-blue-500`;
      case "green":
        return `${baseClasses} bg-green-600 hover:bg-green-700 focus:ring-green-500`;
      case "gray":
        return `${baseClasses} bg-gray-600 hover:bg-gray-700 focus:ring-gray-500`;
      default:
        return `${baseClasses} bg-red-600 hover:bg-red-700 focus:ring-red-500`;
    }
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && !isLoading) {
      onClose();
    }
  };

  const handleConfirm = () => {
    if (!isLoading) {
      onConfirm();
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black/20 transition-opacity"
          onClick={handleBackdropClick}
        />

        {/* Modal */}
        <div className="relative w-full max-w-md bg-white rounded-lg shadow-xl">
          {/* Header */}
          <div className="flex items-center p-4 border-b border-gray-200">
            <div className="flex-shrink-0">
              <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-medium text-gray-900">{title}</h3>
            </div>
          </div>

          {/* Content */}
          <div className="p-4">
            <p className="text-sm text-gray-600">{message}</p>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3 p-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-400 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {cancelText}
            </button>
            <button
              type="button"
              onClick={handleConfirm}
              disabled={isLoading}
              className={getConfirmButtonClasses()}
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Procesando...
                </div>
              ) : (
                confirmText
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

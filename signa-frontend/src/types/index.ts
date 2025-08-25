// Tipos para la aplicación Signa Frontend

// Re-exportar tipos de la API
export * from "./api";

// Tipos específicos de la aplicación
export interface User {
  id: number;
  name: string;
  surname: string;
  email: string;
  address: string;
  status: boolean;
}

export interface Sign {
  id: number;
  sign_name: string;
  status: boolean;
}

export interface SignWithUser {
  sign: Sign;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    name: string;
    surname: string;
    email: string;
    username: string;
  };
}

export interface CreateSignData {
  sign_name: string;
  name: string;
  surname: string;
  email: string;
  address: string;
}

export interface CreateSignResponse {
  message: string;
  sign: Sign;
  user: User;
  user_created: boolean;
  credentials_created: boolean;
  note: string;
}

export interface UpdateSignData {
  sign_name?: string;
  name?: string;
  surname?: string;
  email?: string;
  address?: string;
  password?: string;
}

export interface UpdateSignResponse {
  message: string;
  sign: Sign;
  user: User;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  status_code: number;
}

export type Step = 1 | 2 | 3;

export interface StepperProps {
  currentStep: Step;
  steps: {
    id: Step;
    title: string;
    description: string;
  }[];
}

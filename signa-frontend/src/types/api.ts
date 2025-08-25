// Tipos para las respuestas de la API

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  status_code: number;
}

export interface CreateSignRequest {
  sign_name: string;
  name: string;
  surname: string;
  email: string;
  address: string;
}

export interface UpdateSignRequest {
  sign_name?: string;
  name?: string;
  surname?: string;
  email?: string;
  address?: string;
}

export interface SignWithUser {
  sign: {
    id: number;
    sign_name: string;
    status: boolean;
  };
  user: {
    id: number;
    name: string;
    surname: string;
    email: string;
    address: string;
    status: boolean;
  };
}

export interface SignResponse {
  message: string;
  sign: {
    id: number;
    sign_name: string;
    status: boolean;
  };
  user: {
    id: number;
    name: string;
    surname: string;
    email: string;
    address: string;
    status: boolean;
  };
  user_created?: boolean;
  credentials_created?: boolean;
  note?: string;
}

export interface SignsListResponse {
  success: boolean;
  data: Array<{
    sign: {
      id: number;
      sign_name: string;
      status: boolean;
    };
    user: {
      id: number;
      name: string;
      surname: string;
      email: string;
      address: string;
      status: boolean;
    };
  }>;
  status_code: number;
}

export interface UserResponse {
  id: number;
  name: string;
  surname: string;
  email: string;
  username: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  token_type: string;
  expires_in: number;
  user: UserResponse;
}

export interface ErrorResponse {
  error: string;
  message?: string;
  status_code?: number;
}

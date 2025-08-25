// Servicio de API para comunicarse con el backend

import {
  LoginRequest,
  LoginResponse,
  SignWithUser,
  CreateSignRequest,
  UpdateSignRequest,
  SignResponse,
  SignsListResponse,
  UserResponse,
  ErrorResponse,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem("access_token");
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData: ErrorResponse = await response
        .json()
        .catch(() => ({ error: "Error desconocido" }));
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }
    return response.json();
  }

  // Autenticación
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });
    return this.handleResponse<LoginResponse>(response);
  }

  // Marcas
  async createSign(signData: CreateSignRequest): Promise<SignResponse> {
    const response = await fetch(`${API_BASE_URL}/sign/create`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(signData),
    });
    return this.handleResponse<SignResponse>(response);
  }

  async updateSign(
    signId: number,
    updateData: UpdateSignRequest
  ): Promise<SignResponse> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updateData),
    });
    return this.handleResponse<SignResponse>(response);
  }

  async getSigns(): Promise<SignWithUser[]> {
    const response = await fetch(`${API_BASE_URL}/sign/list`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    const data: SignsListResponse =
      await this.handleResponse<SignsListResponse>(response);
    return data.data;
  }

  async getSignById(signId: number): Promise<SignResponse> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<SignResponse>(response);
  }

  async deleteSign(signId: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "DELETE",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<{ message: string }>(response);
  }

  // Usuarios
  async getUsers(): Promise<UserResponse[]> {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<UserResponse[]>(response);
  }

  async getUserById(userId: number): Promise<UserResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<UserResponse>(response);
  }

  async createUser(userData: CreateSignRequest): Promise<SignResponse> {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(userData),
    });
    return this.handleResponse<SignResponse>(response);
  }

  async updateUser(
    userId: number,
    updateData: UpdateSignRequest
  ): Promise<SignResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updateData),
    });
    return this.handleResponse<SignResponse>(response);
  }

  async deleteUser(userId: number): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "DELETE",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<{ message: string }>(response);
  }
}

export const apiService = new ApiService();

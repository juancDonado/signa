// Servicio de API para comunicarse con el backend

import { LoginResponse, SignWithUser } from "@/types";

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
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.error || `HTTP error! status: ${response.status}`
      );
    }
    return response.json();
  }

  // Autenticación
  async login(credentials: {
    username: string;
    password: string;
  }): Promise<LoginResponse> {
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
  async createSign(signData: any): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/sign/create`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(signData),
    });
    return this.handleResponse<any>(response);
  }

  async updateSign(signId: number, updateData: any): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updateData),
    });
    console.log(response);
    return this.handleResponse<any>(response);
  }

  async getSigns(): Promise<SignWithUser[]> {
    const response = await fetch(`${API_BASE_URL}/sign/list`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<SignWithUser[]>(response);
  }

  async getSignById(signId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<any>(response);
  }

  async deleteSign(signId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/sign/${signId}`, {
      method: "DELETE",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<any>(response);
  }

  // Usuarios
  async getUsers(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<any[]>(response);
  }

  async getUserById(userId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<any>(response);
  }

  async createUser(userData: any): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(userData),
    });
    return this.handleResponse<any>(response);
  }

  async updateUser(userId: number, updateData: any): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updateData),
    });
    return this.handleResponse<any>(response);
  }

  async deleteUser(userId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "DELETE",
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<any>(response);
  }
}

export const apiService = new ApiService();

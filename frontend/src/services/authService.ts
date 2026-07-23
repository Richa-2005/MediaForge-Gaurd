import { apiRequest } from "./apiClient";
import type { AuthResponse, AuthUser, LoginPayload, RegisterPayload } from "../types/auth";

export function register(payload: RegisterPayload) {
  return apiRequest<AuthResponse>("/api/v1/auth/register", {
    method: "POST",
    auth: false,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    errorMessage: "The account could not be created.",
  });
}

export function login(payload: LoginPayload) {
  return apiRequest<AuthResponse>("/api/v1/auth/login", {
    method: "POST",
    auth: false,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    errorMessage: "The login request could not be completed.",
  });
}

export function getCurrentUser() {
  return apiRequest<AuthUser>("/api/v1/auth/me", {
    errorMessage: "The current user could not be loaded.",
  });
}

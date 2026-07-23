import { clearStoredToken, getStoredToken } from "./tokenStore";

const apiBase = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "";

type ApiRequestOptions = RequestInit & {
  auth?: boolean;
  errorMessage?: string;
};

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const { auth = true, errorMessage, headers, ...init } = options;
  const requestHeaders = new Headers(headers);

  if (auth) {
    const token = getStoredToken();
    if (token) {
      requestHeaders.set("Authorization", `Bearer ${token}`);
    }
  }

  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: requestHeaders,
  });
  const payload: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    if (response.status === 401 && auth) {
      clearStoredToken();
      const redirect = encodeURIComponent(
        `${window.location.pathname}${window.location.search}`,
      );
      if (window.location.pathname !== "/login") {
        window.location.assign(`/login?redirect=${redirect}`);
      }
    }

    const detail = typeof payload === "object" && payload !== null && "detail" in payload
      ? String(payload.detail)
      : errorMessage ?? "The request could not be completed.";
    throw new Error(detail);
  }

  return payload as T;
}

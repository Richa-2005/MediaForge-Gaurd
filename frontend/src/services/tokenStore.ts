const tokenKey = "mediaforge_guard_token";

export function getStoredToken() {
  return window.localStorage.getItem(tokenKey);
}

export function storeToken(token: string) {
  window.localStorage.setItem(tokenKey, token);
}

export function clearStoredToken() {
  window.localStorage.removeItem(tokenKey);
}

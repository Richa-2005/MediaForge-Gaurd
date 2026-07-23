import { createContext, ReactNode, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { getCurrentUser, login, register } from "../services/authService";
import { clearStoredToken, getStoredToken, storeToken } from "../services/tokenStore";
import type { AuthUser, LoginPayload, RegisterPayload } from "../types/auth";

type AuthStatus = "loading" | "authenticated" | "anonymous";

type AuthContextValue = {
  user: AuthUser | null;
  status: AuthStatus;
  signIn: (payload: LoginPayload) => Promise<void>;
  signUp: (payload: RegisterPayload) => Promise<void>;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [status, setStatus] = useState<AuthStatus>("loading");

  useEffect(() => {
    let mounted = true;

    if (!getStoredToken()) {
      setStatus("anonymous");
      return;
    }

    getCurrentUser()
      .then((currentUser) => {
        if (!mounted) return;
        setUser(currentUser);
        setStatus("authenticated");
      })
      .catch(() => {
        if (!mounted) return;
        clearStoredToken();
        setUser(null);
        setStatus("anonymous");
      });

    return () => {
      mounted = false;
    };
  }, []);

  const signIn = useCallback(async (payload: LoginPayload) => {
    const response = await login(payload);
    storeToken(response.access_token);
    setUser(response.user);
    setStatus("authenticated");
  }, []);

  const signUp = useCallback(async (payload: RegisterPayload) => {
    const response = await register(payload);
    storeToken(response.access_token);
    setUser(response.user);
    setStatus("authenticated");
  }, []);

  const signOut = useCallback(() => {
    clearStoredToken();
    setUser(null);
    setStatus("anonymous");
    window.location.assign("/");
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({ user, status, signIn, signUp, signOut }),
    [user, status, signIn, signUp, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);

  if (!value) {
    throw new Error("useAuth must be used within AuthProvider.");
  }

  return value;
}

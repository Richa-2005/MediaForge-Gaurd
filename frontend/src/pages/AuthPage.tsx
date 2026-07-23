import { FormEvent, useMemo, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";

type AuthMode = "login" | "register";

function redirectTarget() {
  const requested = new URLSearchParams(window.location.search).get("redirect");
  return requested && requested.startsWith("/") ? requested : "/dashboard";
}

export function AuthPage() {
  const { signIn, signUp } = useAuth();
  const [mode, setMode] = useState<AuthMode>(
    window.location.pathname === "/register" ? "register" : "login",
  );
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const copy = useMemo(
    () => mode === "login"
      ? {
        eyebrow: "Analyst sign in",
        title: "Access your investigations.",
        body: "Sign in to upload media, follow processing, and review the investigations attached to your account.",
        action: "Sign in",
        switchText: "Need an account?",
        switchAction: "Create one",
      }
      : {
        eyebrow: "Create account",
        title: "Start a protected workspace.",
        body: "Create an analyst account so submitted media and results are tied to your authenticated session.",
        action: "Create account",
        switchText: "Already have an account?",
        switchAction: "Sign in",
      },
    [mode],
  );

  const toggleMode = () => {
    const nextMode = mode === "login" ? "register" : "login";
    window.history.replaceState(null, "", `/${nextMode}${window.location.search}`);
    setMode(nextMode);
    setError(null);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      if (mode === "login") {
        await signIn({ email, password });
      } else {
        await signUp({
          email,
          password,
          full_name: fullName.trim() || undefined,
        });
      }
      window.location.assign(redirectTarget());
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Authentication failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="site-shell auth-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        <section className="auth-section section">
          <div className="container auth-layout">
            <div className="auth-copy">
              <p className="eyebrow">{copy.eyebrow}</p>
              <h1>{copy.title}</h1>
              <p>{copy.body}</p>
            </div>

            <form className="auth-form" onSubmit={handleSubmit}>
              {mode === "register" && (
                <label>
                  Full name
                  <input
                    autoComplete="name"
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    placeholder="Media Analyst"
                  />
                </label>
              )}

              <label>
                Email
                <input
                  required
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="analyst@example.com"
                />
              </label>

              <label>
                Password
                <input
                  required
                  type="password"
                  minLength={mode === "register" ? 8 : 1}
                  autoComplete={mode === "register" ? "new-password" : "current-password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder={mode === "register" ? "At least 8 characters" : "Password"}
                />
              </label>

              {error && <p className="auth-form__error" role="alert">{error}</p>}

              <button className="button button--primary" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Working..." : copy.action}
              </button>

              <p className="auth-form__switch">
                {copy.switchText}{" "}
                <button type="button" className="quiet-button" onClick={toggleMode}>
                  {copy.switchAction}
                </button>
              </p>
            </form>
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

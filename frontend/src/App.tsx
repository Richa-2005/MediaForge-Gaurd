import type { ReactElement } from "react";
import { AnalysisCoverage } from "./components/AnalysisCoverage";
import { ClosingCta } from "./components/ClosingCta";
import { Hero } from "./components/Hero";
import { InterpretationSection } from "./components/InterpretationSection";
import { SiteFooter } from "./components/SiteFooter";
import { SiteHeader } from "./components/SiteHeader";
import { Workflow } from "./components/Workflow";
import { UploadPage } from "./pages/UploadPage";
import { InvestigationDashboardPage } from "./pages/InvestigationDashboardPage";
import { AnalysisProgressPage } from "./pages/AnalysisProgressPage";
import { AnalysisResultsPage } from "./pages/AnalysisResultsPage";
import { UploadHistoryPage } from "./pages/UploadHistoryPage";
import { AboutPage } from "./pages/AboutPage";
import { AuthPage } from "./pages/AuthPage";
import { useAuth } from "./auth/AuthContext";

const protectedPaths = new Set([
  "/dashboard",
  "/progress",
  "/results",
  "/upload",
  "/uploads",
]);

function AuthGate({ children }: { children: ReactElement }) {
  const { status } = useAuth();

  if (status === "loading") {
    return (
      <div className="site-shell">
        <main>
          <section className="dashboard-loading section">
            <div className="container"><span /><span /><span /></div>
          </section>
        </main>
      </div>
    );
  }

  if (status === "anonymous") {
    const redirect = encodeURIComponent(`${window.location.pathname}${window.location.search}`);
    window.location.replace(`/login?redirect=${redirect}&reason=auth-required`);
    return (
      <div className="site-shell">
        <main>
          <section className="progress-empty section">
            <div className="container"><p>Redirecting to sign in.</p></div>
          </section>
        </main>
      </div>
    );
  }

  return children;
}

export default function App() {
  const path = window.location.pathname;

  if (path === "/login" || path === "/register") {
    return <AuthPage />;
  }

  const protect = (page: ReactElement) => (
    protectedPaths.has(path) ? <AuthGate>{page}</AuthGate> : page
  );

  if (window.location.pathname === "/upload") {
    return protect(<UploadPage />);
  }

  if (window.location.pathname === "/dashboard") {
    return protect(<InvestigationDashboardPage />);
  }

  if (window.location.pathname === "/progress") {
    return protect(<AnalysisProgressPage />);
  }

  if (window.location.pathname === "/results") {
    return protect(<AnalysisResultsPage />);
  }

  if (window.location.pathname === "/uploads") {
    return protect(<UploadHistoryPage />);
  }

  if (window.location.pathname === "/about") {
    return <AboutPage />;
  }

  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <SiteHeader />
      <main id="main-content">
        <Hero />
        <Workflow />
        <AnalysisCoverage />
        <InterpretationSection />
        <ClosingCta />
      </main>
      <SiteFooter />
    </div>
  );
}

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

export default function App() {
  if (window.location.pathname === "/upload") {
    return <UploadPage />;
  }

  if (window.location.pathname === "/dashboard") {
    return <InvestigationDashboardPage />;
  }

  if (window.location.pathname === "/progress") {
    return <AnalysisProgressPage />;
  }

  if (window.location.pathname === "/results") {
    return <AnalysisResultsPage />;
  }

  if (window.location.pathname === "/uploads") {
    return <UploadHistoryPage />;
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

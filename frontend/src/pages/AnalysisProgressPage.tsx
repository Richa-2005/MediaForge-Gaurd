import { useEffect, useState } from "react";
import { InvestigationHeader } from "../components/InvestigationHeader";
import { InvestigationPipeline } from "../components/InvestigationPipeline";
import { ProcessingActivity } from "../components/ProcessingActivity";
import { ProgressStatePanel } from "../components/ProgressStatePanel";
import { ReportGenerationState } from "../components/ReportGenerationState";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { getUploadSummary } from "../services/dashboardService";
import type { UploadSummary } from "../types/dashboard";
import { isInvestigationFinished } from "../utils/investigation";

function queryUploadId() {
  const value = new URLSearchParams(window.location.search).get("uploadId");
  const id = Number(value);
  return Number.isInteger(id) && id > 0 ? id : null;
}

export function AnalysisProgressPage() {
  const uploadId = queryUploadId();
  const [summary, setSummary] = useState<UploadSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!uploadId) return;
    let mounted = true;
    const load = () => getUploadSummary(uploadId)
      .then((result) => mounted && setSummary(result))
      .catch((requestError) => mounted && setError(requestError instanceof Error ? requestError.message : "The investigation could not be loaded."));
    void load();
    return () => { mounted = false; };
  }, [uploadId]);

  useEffect(() => {
    if (!summary || isInvestigationFinished(summary)) return;
    const interval = window.setInterval(() => {
      getUploadSummary(summary.upload.id).then(setSummary).catch(() => undefined);
    }, 4000);
    return () => window.clearInterval(interval);
  }, [summary]);

  return (
    <div className="site-shell progress-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        {!uploadId && <section className="progress-empty section"><div className="container"><p className="eyebrow">Analysis progress</p><h1>Choose a submission to follow.</h1><p>Progress is available after MediaForge Guard returns an upload ID.</p><a className="button button--primary" href="/upload">Upload &amp; Analyze</a></div></section>}
        {uploadId && !summary && !error && <section className="dashboard-loading section"><div className="container"><span /><span /><span /></div></section>}
        {error && <section className="dashboard-error section"><div className="container"><p role="alert">{error}</p></div></section>}
        {summary && <section className="progress-page__workspace section"><div className="container progress-workspace"><InvestigationHeader summary={summary} /><ProgressStatePanel summary={summary} /><InvestigationPipeline summary={summary} /><ProcessingActivity summary={summary} /><ReportGenerationState summary={summary} /></div></section>}
      </main>
      <SiteFooter />
    </div>
  );
}

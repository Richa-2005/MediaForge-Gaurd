import { useEffect, useState } from "react";
import { AnalysisBreakdown } from "../components/AnalysisBreakdown";
import { EvidenceFindings } from "../components/EvidenceFindings";
import { EvidenceMap } from "../components/EvidenceMap";
import { ForensicTimeline } from "../components/ForensicTimeline";
import { ReportPreview } from "../components/ReportPreview";
import { ResultsActionBar } from "../components/ResultsActionBar";
import { ResultsCaseFile } from "../components/ResultsCaseFile";
import { ResultsHeader } from "../components/ResultsHeader";
import { ResultsSummaryCard } from "../components/ResultsSummaryCard";
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

export function AnalysisResultsPage() {
  const uploadId = queryUploadId();
  const [summary, setSummary] = useState<UploadSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!uploadId) return;
    let mounted = true;
    getUploadSummary(uploadId)
      .then((result) => mounted && setSummary(result))
      .catch((requestError) => mounted && setError(requestError instanceof Error ? requestError.message : "The investigation results could not be loaded."));
    return () => { mounted = false; };
  }, [uploadId]);

  useEffect(() => {
    if (!summary || isInvestigationFinished(summary)) return;
    const interval = window.setInterval(() => { getUploadSummary(summary.upload.id).then(setSummary).catch(() => undefined); }, 4000);
    return () => window.clearInterval(interval);
  }, [summary]);

  return (
    <div className="site-shell results-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        {!uploadId && <section className="progress-empty section"><div className="container"><p className="eyebrow">Analysis results</p><h1>Choose an investigation to review.</h1><p>Results become available after MediaForge Guard returns an upload ID and analysis output.</p><a className="button button--primary" href="/dashboard">Open dashboard</a></div></section>}
        {uploadId && !summary && !error && <section className="dashboard-loading section"><div className="container"><span /><span /><span /></div></section>}
        {error && <section className="dashboard-error section"><div className="container"><p role="alert">{error}</p></div></section>}
        {summary && <><ResultsActionBar summary={summary} /><section className="results-page__workspace section"><div className="container results-workspace"><ResultsHeader summary={summary} /><ResultsCaseFile summary={summary} /><section id="investigation-summary"><ResultsSummaryCard summary={summary} /></section><EvidenceMap summary={summary} /><ForensicTimeline summary={summary} /><EvidenceFindings summary={summary} /><AnalysisBreakdown summary={summary} /><ReportPreview summary={summary} /></div></section></>}
      </main>
      <SiteFooter />
    </div>
  );
}

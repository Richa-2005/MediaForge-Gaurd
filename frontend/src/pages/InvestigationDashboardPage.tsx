import { useEffect, useState } from "react";
import { AnalysisBreakdown } from "../components/AnalysisBreakdown";
import { EvidenceFindings } from "../components/EvidenceFindings";
import { InvestigationHeader } from "../components/InvestigationHeader";
import { InvestigationPipeline } from "../components/InvestigationPipeline";
import { InvestigationSelector } from "../components/InvestigationSelector";
import { InvestigationStatusOverview } from "../components/InvestigationStatusOverview";
import { ReportPreview } from "../components/ReportPreview";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { getRecentInvestigations, getUploadSummary } from "../services/dashboardService";
import type { UploadSummary } from "../types/dashboard";
import type { UploadRecord } from "../types/upload";

function queryUploadId() {
  const value = new URLSearchParams(window.location.search).get("uploadId");
  const id = Number(value);
  return Number.isInteger(id) && id > 0 ? id : null;
}

export function InvestigationDashboardPage() {
  const [uploads, setUploads] = useState<UploadRecord[] | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(queryUploadId);
  const [summary, setSummary] = useState<UploadSummary | null>(null);
  const [recentError, setRecentError] = useState<string | null>(null);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [isLoadingSummary, setIsLoadingSummary] = useState(false);

  useEffect(() => {
    let mounted = true;
    getRecentInvestigations()
      .then((result) => {
        if (!mounted) return;
        setUploads(result);
        setSelectedId((current) => current ?? result[0]?.id ?? null);
      })
      .catch(() => mounted && setRecentError("Recent investigations are unavailable right now."));
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    if (!selectedId) {
      setSummary(null);
      return;
    }
    let mounted = true;
    setIsLoadingSummary(true);
    setSummaryError(null);
    getUploadSummary(selectedId)
      .then((result) => mounted && setSummary(result))
      .catch((error) => mounted && setSummaryError(error instanceof Error ? error.message : "The investigation could not be loaded."))
      .finally(() => mounted && setIsLoadingSummary(false));
    return () => { mounted = false; };
  }, [selectedId]);

  useEffect(() => {
    if (!summary || !["queued", "processing"].includes(summary.upload.status)) return;
    const interval = window.setInterval(() => {
      getUploadSummary(summary.upload.id)
        .then((result) => setSummary(result))
        .catch(() => undefined);
    }, 4000);
    return () => window.clearInterval(interval);
  }, [summary]);

  const selectInvestigation = (uploadId: number) => {
    window.history.replaceState(null, "", `/dashboard?uploadId=${uploadId}`);
    setSelectedId(uploadId);
  };

  return (
    <div className="site-shell dashboard-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        <section className="dashboard-page__selector section">
          <div className="container"><InvestigationSelector uploads={uploads} selectedId={selectedId} onSelect={selectInvestigation} loading={uploads === null && !recentError} error={recentError} /></div>
        </section>

        {isLoadingSummary && <section className="dashboard-loading section"><div className="container"><span /><span /><span /></div></section>}
        {summaryError && <section className="dashboard-error section"><div className="container"><p role="alert">{summaryError}</p></div></section>}
        {summary && (
          <section className="dashboard-page__workspace section">
            <div className="container dashboard-workspace">
              <InvestigationHeader summary={summary} />
              <InvestigationStatusOverview summary={summary} />
              <InvestigationPipeline summary={summary} />
              <EvidenceFindings summary={summary} />
              <AnalysisBreakdown summary={summary} />
              <ReportPreview summary={summary} />
            </div>
          </section>
        )}
      </main>
      <SiteFooter />
    </div>
  );
}

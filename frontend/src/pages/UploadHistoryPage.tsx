import { useEffect, useMemo, useState } from "react";
import { HistoryFilters } from "../components/HistoryFilters";
import { HistoryList } from "../components/HistoryList";
import { HistoryPreview } from "../components/HistoryPreview";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { getUploadSummary } from "../services/dashboardService";
import { getRecentUploads } from "../services/uploadService";
import type { UploadSummary } from "../types/dashboard";
import type { UploadRecord, UploadStatus } from "../types/upload";

export function UploadHistoryPage() {
  const [uploads, setUploads] = useState<UploadRecord[] | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [summary, setSummary] = useState<UploadSummary | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [isSummaryLoading, setIsSummaryLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [mediaType, setMediaType] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    let mounted = true;
    getRecentUploads()
      .then((result) => { if (mounted) setUploads(result); })
      .catch(() => mounted && setHistoryError("The recent investigation archive is unavailable right now."));
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    if (!selectedId) { setSummary(null); return; }
    let mounted = true;
    setIsSummaryLoading(true);
    setSummaryError(null);
    getUploadSummary(selectedId)
      .then((result) => mounted && setSummary(result))
      .catch((error) => mounted && setSummaryError(error instanceof Error ? error.message : "The selected investigation could not be loaded."))
      .finally(() => mounted && setIsSummaryLoading(false));
    return () => { mounted = false; };
  }, [selectedId]);

  const mediaTypes = useMemo(() => [...new Set((uploads ?? []).map((upload) => upload.media_type))], [uploads]);
  const statuses = useMemo(() => [...new Set((uploads ?? []).map((upload) => upload.status))] as UploadStatus[], [uploads]);
  const filtered = useMemo(() => (uploads ?? []).filter((upload) => upload.original_filename.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()) && (!mediaType || upload.media_type === mediaType) && (!status || upload.status === status)), [uploads, query, mediaType, status]);

  return (
    <div className="site-shell history-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        <section className="history-page__workspace section"><div className="container"><header className="history-header"><div><p className="eyebrow">Investigation archive</p><h1>Recent media investigations.</h1><p>The service currently returns its most recent submissions. Search and filters apply to this available archive.</p></div><a className="button button--primary" href="/upload">New investigation</a></header>
          <HistoryFilters query={query} mediaType={mediaType} status={status} mediaTypes={mediaTypes} statuses={statuses} onQueryChange={setQuery} onMediaTypeChange={setMediaType} onStatusChange={setStatus} />
          {uploads === null && !historyError && <div className="history-loading" aria-label="Loading recent investigation history"><span /><span /><span /></div>}
          {historyError && <p className="history-error" role="alert">{historyError}</p>}
          {uploads && <div className="history-page__content"><HistoryList uploads={filtered} selectedId={selectedId} onSelect={setSelectedId} /><HistoryPreview summary={summary} loading={isSummaryLoading} error={summaryError} /></div>}
        </div></section>
      </main>
      <SiteFooter />
    </div>
  );
}

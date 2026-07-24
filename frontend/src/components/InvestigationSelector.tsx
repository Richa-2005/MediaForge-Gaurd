import type { UploadRecord } from "../types/upload";
import { StatusBadge } from "./StatusBadge";
import { InvestigationBoardBackdrop } from "./InvestigationBoardBackdrop";

type InvestigationSelectorProps = {
  uploads: UploadRecord[] | null;
  selectedId: number | null;
  onSelect: (uploadId: number) => void;
  loading: boolean;
  error: string | null;
};

export function InvestigationSelector({ uploads, selectedId, onSelect, loading, error }: InvestigationSelectorProps) {
  return (
    <section className="investigation-selector" aria-labelledby="investigation-selector-title">
      <InvestigationBoardBackdrop />
      <div className="investigation-selector__heading">
        <div>
          <p className="eyebrow">Investigation dashboard</p>
          <h1 id="investigation-selector-title">Review an active investigation.</h1>
        </div>
        <a className="button button--primary" href="/upload">New investigation</a>
      </div>
      <p className="investigation-selector__copy">Select a recent submission to inspect the processing record, available evidence, specialist findings, and report status.</p>

      {loading && <div className="selector-loading" aria-label="Loading recent investigations"><span /><span /><span /></div>}
      {error && <p className="selector-message" role="alert">{error}</p>}
      {uploads?.length === 0 && <p className="selector-message">No submitted media is available to investigate yet.</p>}
      {uploads && uploads.length > 0 && (
        <div className="investigation-selector__list" aria-label="Recent investigations">
          {uploads.map((upload) => (
            <button
              key={upload.id}
              className={`investigation-choice ${selectedId === upload.id ? "investigation-choice--selected" : ""}`}
              type="button"
              onClick={() => onSelect(upload.id)}
              aria-pressed={selectedId === upload.id}
            >
              <span className="investigation-choice__media">{upload.media_type}</span>
              <span className="investigation-choice__name">{upload.original_filename}</span>
              <StatusBadge status={upload.status} />
            </button>
          ))}
        </div>
      )}
    </section>
  );
}

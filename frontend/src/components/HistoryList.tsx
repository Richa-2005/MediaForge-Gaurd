import type { UploadRecord } from "../types/upload";
import { formatTimestamp } from "../utils/dateTime";
import { StatusBadge } from "./StatusBadge";

type HistoryListProps = { uploads: UploadRecord[]; selectedId: number | null; onSelect: (id: number) => void };

export function HistoryList({ uploads, selectedId, onSelect }: HistoryListProps) {
  if (uploads.length === 0) return <p className="history-empty">No returned submissions match the current filters.</p>;

  return (
    <div className="history-list" aria-label="Recent investigation archive">
      {uploads.map((upload) => (
        <button className={`history-card ${selectedId === upload.id ? "history-card--selected" : ""}`} type="button" key={upload.id} onClick={() => onSelect(upload.id)} aria-pressed={selectedId === upload.id}>
          <span className="history-card__media">{upload.media_type}</span>
          <span className="history-card__main"><strong>{upload.original_filename}</strong><small>{formatTimestamp(upload.created_at)}</small></span>
          <StatusBadge status={upload.status} />
          <span className="history-card__id">#{upload.id}</span>
        </button>
      ))}
    </div>
  );
}

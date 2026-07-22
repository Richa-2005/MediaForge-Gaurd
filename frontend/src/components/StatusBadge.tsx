import type { StatusValue } from "../types/dashboard";
import type { UploadStatus } from "../types/upload";

type StatusBadgeProps = {
  status: StatusValue | UploadStatus;
  label?: string;
};

export function StatusBadge({ status, label }: StatusBadgeProps) {
  return <span className={`status-badge status-badge--${status}`}>{label ?? status.replace(/-/g, " ")}</span>;
}

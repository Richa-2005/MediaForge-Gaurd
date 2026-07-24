import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult } from "../utils/investigation";

export function EvidenceMap({ summary }: { summary: UploadSummary }) {
  const primary = getPrimaryResult(summary);
  const hasPreprocessing = summary.processing_steps.some((step) => step.step_name === "preprocessing" && step.status === "completed");
  const evidenceCount = summary.analysis_results.reduce((total, result) => total + (result.evidence?.length ?? 0), 0);
  const nodes = [
    { label: "Upload", active: true },
    { label: "Preprocessing", active: hasPreprocessing },
    { label: "Agents", active: summary.analysis_results.length > 0 },
    { label: "Evidence", active: evidenceCount > 0 },
    { label: "Verdict", active: Boolean(primary) },
  ];

  return (
    <section className="evidence-map scroll-reveal" aria-labelledby="evidence-map-title">
      <div className="section-heading-row">
        <div>
          <p className="eyebrow">Animated evidence map</p>
          <h2 id="evidence-map-title">How the verdict was assembled.</h2>
        </div>
        <span>{evidenceCount} evidence item{evidenceCount === 1 ? "" : "s"}</span>
      </div>
      <div className="evidence-map__nodes" aria-label="Upload to verdict evidence path">
        {nodes.map((node, index) => (
          <div className={`evidence-map__node ${node.active ? "evidence-map__node--active" : ""}`} key={node.label}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <strong>{node.label}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

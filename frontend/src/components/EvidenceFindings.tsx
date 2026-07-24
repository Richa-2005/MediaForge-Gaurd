import type { AnalysisResult, Evidence, ProcessingArtifact, UploadSummary } from "../types/dashboard";
import { StateIllustration } from "./StateIllustration";

type EvidenceEntry = Evidence & { agent: AnalysisResult["agent"]; resultId: number };

function evidenceEntries(results: AnalysisResult[]) {
  return results.flatMap((result) => (result.evidence ?? []).map((evidence) => ({ ...evidence, agent: result.agent, resultId: result.id })));
}

function renderMetadata(metadata: Record<string, unknown> | undefined) {
  if (!metadata || Object.keys(metadata).length === 0) return null;
  return <details><summary>Metadata</summary><dl>{Object.entries(metadata).map(([key, value]) => <div key={key}><dt>{key.replace(/_/g, " ")}</dt><dd>{typeof value === "string" || typeof value === "number" || typeof value === "boolean" ? String(value) : JSON.stringify(value)}</dd></div>)}</dl></details>;
}

function EvidenceCard({ evidence }: { evidence: EvidenceEntry }) {
  return <article className="evidence-card"><div className="evidence-card__top"><span>{evidence.agent}</span>{evidence.method && <strong>{evidence.method}</strong>}</div>{evidence.summary && <p>{evidence.summary}</p>}<div className="evidence-card__scores">{typeof evidence.score === "number" && <span>Score {Math.round(evidence.score * 100)}%</span>}{typeof evidence.confidence === "number" && <span>Confidence {Math.round(evidence.confidence * 100)}%</span>}</div>{renderMetadata(evidence.metadata)}</article>;
}

function ArtifactCard({ artifact }: { artifact: ProcessingArtifact }) {
  return <article className="artifact-card"><span>{artifact.artifact_type.replace(/_/g, " ")}</span>{artifact.details && <p>{Object.entries(artifact.details).map(([key, value]) => `${key.replace(/_/g, " ")}: ${typeof value === "string" || typeof value === "number" ? value : JSON.stringify(value)}`).join(" · ")}</p>}</article>;
}

export function EvidenceFindings({ summary }: { summary: UploadSummary }) {
  const evidence = evidenceEntries(summary.analysis_results);
  return (
    <section className="evidence-findings scroll-reveal" aria-labelledby="evidence-findings-title">
      <div className="evidence-findings__heading"><div><p className="eyebrow">Evidence & findings</p><h2 id="evidence-findings-title">What the investigation has returned.</h2></div><span>{evidence.length} evidence item{evidence.length === 1 ? "" : "s"}</span></div>
      {evidence.length > 0 ? <div className="evidence-findings__grid">{evidence.map((item, index) => <EvidenceCard key={`${item.resultId}-${item.method ?? "evidence"}-${index}`} evidence={item} />)}</div> : <div className="dashboard-empty dashboard-empty--illustrated"><StateIllustration kind="evidence" /><p>No evidence has been returned by the available analysis results yet.</p></div>}
      {summary.artifacts.length > 0 && <div className="artifact-area"><p className="artifact-area__label">Processing artifacts</p><div>{summary.artifacts.map((artifact) => <ArtifactCard key={artifact.id} artifact={artifact} />)}</div></div>}
    </section>
  );
}

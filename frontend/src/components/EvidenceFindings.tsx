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
  const score = typeof evidence.score === "number" ? Math.round(evidence.score * 100) : null;
  const confidence = typeof evidence.confidence === "number" ? Math.round(evidence.confidence * 100) : null;
  return <article className="evidence-card"><div className="evidence-card__pin" aria-hidden="true" /><div className="evidence-card__top"><span>{evidence.agent}</span>{evidence.method && <strong>{evidence.method}</strong>}</div>{evidence.summary && <p>{evidence.summary}</p>}<div className="evidence-card__scores">{score !== null && <span>Score {score}%</span>}{confidence !== null && <span>Confidence {confidence}%</span>}</div><div className="evidence-card__signal" aria-hidden="true"><span style={{ height: `${Math.max(score ?? 22, 10)}%` }} /><span style={{ height: `${Math.max(confidence ?? 34, 10)}%` }} /><span style={{ height: `${Math.max(((score ?? 35) + (confidence ?? 35)) / 2, 10)}%` }} /></div>{evidence.artifact_path && <a className="evidence-card__artifact" href={evidence.artifact_path}>Artifact path</a>}{renderMetadata(evidence.metadata)}</article>;
}

function ArtifactCard({ artifact }: { artifact: ProcessingArtifact }) {
  const details = Object.entries(artifact.details ?? {});
  return <article className="artifact-card"><span>{artifact.artifact_type.replace(/_/g, " ")}</span>{details.length > 0 && <p>{details.map(([key, value]) => `${key.replace(/_/g, " ")}: ${typeof value === "string" || typeof value === "number" ? value : JSON.stringify(value)}`).join(" · ")}</p>}</article>;
}

function displayArtifacts(artifacts: ProcessingArtifact[]) {
  const frameCount = artifacts.filter((artifact) => artifact.artifact_type === "frame").length;
  const visible = artifacts.filter((artifact) => {
    if (artifact.artifact_type === "frame") return false;
    return Object.keys(artifact.details ?? {}).length > 0 || artifact.artifact_type !== "processed_audio";
  });

  if (frameCount > 0) {
    visible.push({
      id: -1,
      upload_id: artifacts[0]?.upload_id ?? 0,
      artifact_type: "sampled_video_frames",
      file_path: null,
      details: { frames_extracted: frameCount },
      created_at: artifacts[0]?.created_at ?? "",
    });
  }

  return visible;
}

export function EvidenceFindings({ summary }: { summary: UploadSummary }) {
  const evidence = evidenceEntries(summary.analysis_results);
  const artifacts = displayArtifacts(summary.artifacts);
  return (
    <section className="evidence-findings scroll-reveal" aria-labelledby="evidence-findings-title">
      <div className="evidence-findings__heading"><div><p className="eyebrow">Evidence & findings</p><h2 id="evidence-findings-title">What the investigation has returned.</h2></div><span>{evidence.length} evidence item{evidence.length === 1 ? "" : "s"}</span></div>
      {evidence.length > 0 ? <div className="evidence-findings__grid evidence-wall">{evidence.map((item, index) => <EvidenceCard key={`${item.resultId}-${item.method ?? "evidence"}-${index}`} evidence={item} />)}</div> : <div className="dashboard-empty dashboard-empty--illustrated"><StateIllustration kind="evidence" /><p>No evidence has been returned by the available analysis results yet.</p></div>}
      {artifacts.length > 0 && <div className="artifact-area"><p className="artifact-area__label">Processing artifacts</p><div>{artifacts.map((artifact) => <ArtifactCard key={artifact.id} artifact={artifact} />)}</div></div>}
    </section>
  );
}

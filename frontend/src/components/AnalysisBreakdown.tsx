import type { AnalysisAgent, AnalysisResult, UploadSummary } from "../types/dashboard";
import { StatusBadge } from "./StatusBadge";

const labels: Record<AnalysisAgent, string> = { text: "Text analysis", vision: "Image analysis", video: "Video analysis", audio: "Audio analysis", factcheck: "Fact checking", supervisor: "Supervisory assessment" };
const order: AnalysisAgent[] = ["text", "vision", "video", "audio", "factcheck", "supervisor"];

function AnalysisModule({ result }: { result: AnalysisResult }) {
  return <article className="analysis-module"><div className="analysis-module__top"><h3>{labels[result.agent]}</h3><StatusBadge status={result.label} /></div><p>{result.explanation ?? "No explanation supplied."}</p><dl><div><dt>Confidence</dt><dd>{Math.round(result.confidence * 100)}%</dd></div><div><dt>Risk score</dt><dd>{Math.round(result.risk_score * 100)}%</dd></div><div><dt>Evidence</dt><dd>{result.evidence?.length ?? 0} item{(result.evidence?.length ?? 0) === 1 ? "" : "s"}</dd></div></dl></article>;
}

export function AnalysisBreakdown({ summary }: { summary: UploadSummary }) {
  const byAgent = new Map(summary.analysis_results.map((result) => [result.agent, result]));
  const available = order.map((agent) => byAgent.get(agent)).filter((result): result is AnalysisResult => Boolean(result));
  return <section className="analysis-breakdown scroll-reveal" aria-labelledby="analysis-breakdown-title"><div className="analysis-breakdown__heading"><p className="eyebrow">Media analysis breakdown</p><h2 id="analysis-breakdown-title">Available specialist results.</h2></div>{available.length > 0 ? <div className="analysis-breakdown__grid">{available.map((result) => <AnalysisModule key={result.id} result={result} />)}</div> : <p className="dashboard-empty">No specialist analysis results are available for this submission yet.</p>}</section>;
}

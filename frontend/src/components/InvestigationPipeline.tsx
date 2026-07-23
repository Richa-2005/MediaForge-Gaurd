import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult } from "../utils/investigation";
import { StatusBadge } from "./StatusBadge";

type PipelineState = "completed" | "current" | "pending" | "failed";

function pipelineState(summary: UploadSummary, index: number): PipelineState {
  const preprocessing = summary.processing_steps.find((step) => step.step_name === "preprocessing");
  const hasAnalyses = summary.analysis_results.length > 0;
  const hasEvidence = summary.analysis_results.some((result) => result.evidence?.length) || summary.artifacts.length > 0;
  const hasAssessment = summary.analysis_results.some((result) => typeof result.confidence === "number" && typeof result.risk_score === "number");
  const primaryResult = getPrimaryResult(summary);

  if (summary.upload.status === "failed" || summary.processing_run?.status === "failed" || preprocessing?.status === "failed") return index <= 2 ? "failed" : "pending";
  const states: PipelineState[] = [
    "completed",
    "completed",
    preprocessing?.status === "completed" ? "completed" : preprocessing?.status === "running" || summary.upload.status === "processing" ? "current" : "pending",
    hasAnalyses ? "completed" : summary.upload.status === "processing" ? "current" : "pending",
    hasEvidence && hasAssessment ? "completed" : hasAnalyses ? "current" : "pending",
    primaryResult?.explanation_status === "completed" ? "completed" : primaryResult?.explanation_status === "failed" ? "failed" : hasAssessment ? "current" : "pending",
  ];
  return states[index];
}

const stages = ["Media input", "Media classification", "Preprocessing", "Specialist analysis", "Evidence & assessment", "Structured report"];

export function InvestigationPipeline({ summary }: { summary: UploadSummary }) {
  return (
    <section className="investigation-pipeline scroll-reveal" aria-labelledby="investigation-pipeline-title">
      <div className="investigation-pipeline__heading"><p className="eyebrow">Investigation pipeline</p><h2 id="investigation-pipeline-title">The available processing record.</h2></div>
      <div className="investigation-pipeline__track" aria-label="Investigation progress through available pipeline stages">
        {stages.map((stage, index) => {
          const state = pipelineState(summary, index);
          return <div className={`investigation-pipeline__stage investigation-pipeline__stage--${state}`} key={stage}><span>{String(index + 1).padStart(2, "0")}</span><strong>{stage}</strong><small>{state === "completed" ? "Recorded" : state === "current" ? "In progress" : state === "failed" ? "Stopped" : "Pending"}</small></div>;
        })}
      </div>
      {summary.processing_steps.length > 0 && <div className="investigation-pipeline__steps"><span>Recorded step</span>{summary.processing_steps.map((step) => <div key={step.id}><strong>{step.step_name}</strong><StatusBadge status={step.status} />{step.error_message && <p>{step.error_message}</p>}</div>)}</div>}
    </section>
  );
}

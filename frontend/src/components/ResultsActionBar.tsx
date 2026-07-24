import type { UploadSummary } from "../types/dashboard";
import { getPrimaryResult } from "../utils/investigation";

function summaryText(summary: UploadSummary) {
  const primary = getPrimaryResult(summary);
  const report = primary?.report;
  return report?.executive_summary ?? report?.summary ?? primary?.summary ?? primary?.explanation ?? "No summary supplied.";
}

function fullReportText(summary: UploadSummary) {
  const primary = getPrimaryResult(summary);
  if (primary?.report_markdown) return primary.report_markdown;

  const report = primary?.report;
  const verdict = report?.verdict ?? (primary ? { label: primary.label, confidence: primary.confidence } : null);
  const lines = [
    `# ${report?.title ?? "MediaForge Guard Investigation Report"}`,
    "",
    "## Submission",
    `- File: ${summary.upload.original_filename}`,
    `- Media type: ${summary.upload.media_type}`,
    `- Submission ID: ${summary.upload.id}`,
    `- Status: ${summary.upload.status}`,
    "",
  ];

  if (verdict) {
    lines.push(
      "## Overall Assessment",
      `- Verdict: ${verdict.label}`,
      `- Confidence: ${Math.round(verdict.confidence * 100)}%`,
      primary ? `- Risk score: ${Math.round(primary.risk_score * 100)}%` : "",
      "",
    );
  }

  lines.push("## Executive Summary", summaryText(summary), "");

  if (report?.key_findings?.length) {
    lines.push("## Key Findings", ...report.key_findings.map((finding) => `- ${finding}`), "");
  }

  if (report?.agent_analyses?.length) {
    lines.push("## Agent Analyses");
    report.agent_analyses.forEach((analysis) => {
      lines.push(`### ${analysis.title || analysis.agent}`, analysis.analysis);
      if (analysis.key_observations.length > 0) {
        lines.push("", "Key observations:", ...analysis.key_observations.map((observation) => `- ${observation}`));
      }
      lines.push("");
    });
  }

  if (report?.recommendation) lines.push("## Recommended Action", report.recommendation, "");
  if (report?.limitations) lines.push("## Limitations", report.limitations, "");
  if (report?.technical_notes) lines.push("## Technical Notes", report.technical_notes, "");

  if (!report && primary?.explanation) {
    lines.push("## Available Explanation", primary.explanation, "");
  }

  if (summary.analysis_results.length > 0) {
    lines.push("## Specialist Results");
    summary.analysis_results.forEach((result) => {
      lines.push(
        `### ${result.agent}`,
        `- Label: ${result.label}`,
        `- Confidence: ${Math.round(result.confidence * 100)}%`,
        `- Risk score: ${Math.round(result.risk_score * 100)}%`,
      );
      if (result.summary) lines.push(`- Summary: ${result.summary}`);
      if (result.explanation) lines.push("", result.explanation);
      if (result.evidence?.length) {
        lines.push("", "Evidence:");
        result.evidence.forEach((evidence) => {
          lines.push(`- ${evidence.method ? `${evidence.method}: ` : ""}${evidence.summary ?? "Evidence item"}`);
        });
      }
      lines.push("");
    });
  }

  return [
    ...lines,
  ].filter((line) => line !== "").join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

export function ResultsActionBar({ summary }: { summary: UploadSummary }) {
  const report = fullReportText(summary);
  const summaryCopy = summaryText(summary);

  const downloadReport = () => {
    const blob = new Blob([report], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `mediaforge-report-${summary.upload.id}.md`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const copySummary = async () => {
    await navigator.clipboard.writeText(summaryCopy);
  };

  return (
    <div className="results-action-bar" aria-label="Results actions">
      <button type="button" onClick={downloadReport}>Download report</button>
      <button type="button" onClick={copySummary}>Copy summary</button>
      <a href={`/dashboard?uploadId=${summary.upload.id}`}>Back to dashboard</a>
      <a href="/upload">Analyze another</a>
    </div>
  );
}

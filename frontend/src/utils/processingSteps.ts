import type { ProcessingStep, UploadSummary } from "../types/dashboard";
import type { UploadRecord } from "../types/upload";

const stepLabels: Record<string, string> = {
  queue_assigned: "Queue assigned",
  preprocessing: "Preparing media",
  analysis: "Running specialist analysis",
  report_generation: "Building report",
};

const stepDescriptions: Record<string, string> = {
  queue_assigned: "The submission was assigned to the appropriate media queue.",
  preprocessing: "The service is preparing the media for the relevant analysis path.",
  analysis: "Specialist analysis is running for the submitted media type.",
  report_generation: "The final structured investigation report is being assembled.",
};

export function formatStepName(stepName: string) {
  return stepLabels[stepName] ?? stepName.replace(/_/g, " ");
}

export function describeStep(stepName: string) {
  return stepDescriptions[stepName] ?? "Recorded processing activity.";
}

export function currentStep(summary: UploadSummary): ProcessingStep | undefined {
  return summary.processing_steps.find((step) => step.status === "running")
    ?? summary.processing_steps.find((step) => step.status === "pending")
    ?? summary.processing_steps.at(-1);
}

export function investigationDestination(summary: UploadSummary) {
  if (summary.upload.status === "completed") return `/results?uploadId=${summary.upload.id}`;
  return `/progress?uploadId=${summary.upload.id}`;
}

export function investigationActionLabel(summary: UploadSummary) {
  if (summary.upload.status === "completed") return "Review results";
  if (summary.upload.status === "failed") return "View status";
  return "Follow progress";
}

export function uploadDestination(upload: UploadRecord) {
  if (upload.status === "completed") return `/results?uploadId=${upload.id}`;
  return `/progress?uploadId=${upload.id}`;
}

export function uploadActionLabel(upload: UploadRecord) {
  if (upload.status === "completed") return "Review results";
  if (upload.status === "failed") return "View status";
  return "Follow progress";
}

import { useEffect, useRef, useState } from "react";
import type { CSSProperties } from "react";
import { PipelineDoodle } from "./PipelineDoodle";

const stages = [
  { number: "01", title: "Upload media", summary: "Supported file or public URL", detailTitle: "A single intake, routed by media type.", detail: "The submitted file is MIME-checked, hashed, stored, and queued for processing before analysis begins.", technologies: ["MIME validation", "SHA-256 deduplication", "Queued processing"], doodle: "upload" as const },
  { number: "02", title: "Media router", summary: "The appropriate path is selected", detailTitle: "Each medium follows its own preparation path.", detail: "Images are processed, videos yield sampled frames, audio is prepared for forensic inspection, and text is validated as UTF-8 content.", technologies: ["Image preprocessing", "Frame extraction", "Audio preparation", "UTF-8 text validation"], doodle: "router" as const },
  { number: "03", title: "Specialized analysis", summary: "Purpose-built forensic pipelines", detailTitle: "Different signals are examined for every media path.", detail: "The system runs only the specialists relevant to the submitted media, then returns their available evidence and observations.", technologies: ["Image: ELA · noise · FFT · blur", "Video: per-frame visual analysis", "Audio: spectral · MFCC · transcription", "Text: claims · linguistic signals · verification"], doodle: "analysis" as const },
  { number: "04", title: "Evidence aggregation", summary: "Agent output becomes reviewable evidence", detailTitle: "Outputs are retained with their context.", detail: "Analysis results, evidence items, per-frame details, and processing artifacts are persisted for the submission’s review record.", technologies: ["Agent evidence", "Artifact metadata", "Per-frame results", "Analysis persistence"], doodle: "evidence" as const },
  { number: "05", title: "Confidence & risk assessment", summary: "Decision engines interpret available signals", detailTitle: "Signals are converted into cautious outcomes.", detail: "Specialist decision engines produce a label, risk score, confidence, explanation, and evidence. Text may also receive a supervisor fusion result.", technologies: ["Risk scoring", "Confidence scoring", "Specialist verdicts", "Text supervisor fusion"], doodle: "assessment" as const },
  { number: "06", title: "Structured investigation report", summary: "LangGraph creates the final explanation", detailTitle: "The report explains; it does not alter the verdict.", detail: "The LangGraph workflow collects persisted context, creates a structured explanation, formats Markdown, and stores the consolidated report on the primary result.", technologies: ["LangGraph context collection", "Structured explanation", "Markdown formatting", "Report persistence"], doodle: "report" as const },
];

export function Workflow() {
  const [activeStage, setActiveStage] = useState(0);
  const sectionRef = useRef<HTMLElement | null>(null);
  const active = stages[activeStage];

  useEffect(() => {
    const updateStageFromScroll = () => {
      const section = sectionRef.current;
      if (!section) return;

      const bounds = section.getBoundingClientRect();
      if (bounds.bottom < 0 || bounds.top > window.innerHeight) return;

      const distance = Math.max(section.offsetHeight - window.innerHeight * 0.25, 1);
      const progress = Math.min(1, Math.max(0, (window.innerHeight * 0.55 - bounds.top) / distance));
      setActiveStage(Math.min(stages.length - 1, Math.floor(progress * stages.length)));
    };

    updateStageFromScroll();
    window.addEventListener("scroll", updateStageFromScroll, { passive: true });
    window.addEventListener("resize", updateStageFromScroll);
    return () => {
      window.removeEventListener("scroll", updateStageFromScroll);
      window.removeEventListener("resize", updateStageFromScroll);
    };
  }, []);

  return (
    <section className="workflow section section--wide" aria-labelledby="workflow-title" ref={sectionRef}>
      <div className="container">
        <div className="section-intro section-intro--workflow">
          <p className="eyebrow scroll-reveal">Verification pipeline</p>
          <h2 id="workflow-title" className="scroll-reveal">A complete investigation system, not a single model.</h2>
          <p className="section-intro__copy scroll-reveal">Follow the path from secure media intake through specialized analysis, evidence, assessment, and structured reporting.</p>
        </div>

        <div className="pipeline" style={{ "--pipeline-progress": `${(activeStage / (stages.length - 1)) * 100}%` } as CSSProperties}>
          <div className="pipeline__track" aria-hidden="true"><span /></div>
          <div className="pipeline__sequence" aria-label="Verification pipeline stages">
            {stages.map((stage, index) => (
              <button
                className={`pipeline-stage ${index === activeStage ? "pipeline-stage--active" : ""} ${index < activeStage ? "pipeline-stage--complete" : ""}`}
                key={stage.number}
                type="button"
                aria-pressed={index === activeStage}
                aria-controls="pipeline-detail"
                onClick={() => setActiveStage(index)}
              >
                <span className="pipeline-stage__node"><span>{stage.number}</span></span>
                <span className="pipeline-stage__copy"><strong>{stage.title}</strong><small>{stage.summary}</small></span>
              </button>
            ))}
          </div>
        </div>

        <article className="pipeline-detail" id="pipeline-detail" aria-live="polite">
          <div className="pipeline-detail__illustration" aria-hidden="true"><PipelineDoodle key={active.number} stage={active.doodle} /></div>
          <div className="pipeline-detail__content">
            <p className="pipeline-detail__index">{active.number} / {String(stages.length).padStart(2, "0")}</p>
            <h3>{active.detailTitle}</h3>
            <p>{active.detail}</p>
            <ul aria-label={`${active.title} technologies`}>
              {active.technologies.map((technology) => <li key={technology}>{technology}</li>)}
            </ul>
          </div>
        </article>

        <a className="text-link text-link--section scroll-reveal" href="/upload">Begin an analysis <span aria-hidden="true">→</span></a>
      </div>
    </section>
  );
}

import type { CSSProperties } from "react";
import { EvidenceJudgmentIllustration } from "./EvidenceJudgmentIllustration";

export function InterpretationSection() {
  return (
    <section className="interpretation section" aria-labelledby="interpretation-title">
      <EvidenceJudgmentIllustration />
      <div className="container interpretation__content scroll-reveal">
        <div className="interpretation__label">
          <span aria-hidden="true" />
          <p className="eyebrow type-on-scroll" style={{ "--type-chars": 16 } as CSSProperties}>A careful review</p>
        </div>
        <h2 id="interpretation-title" className="type-on-scroll type-on-scroll--heading" style={{ "--type-chars": 56 } as CSSProperties}>Evidence supports judgment.<br />It does not replace it.</h2>
        <p className="type-on-scroll type-on-scroll--copy" style={{ "--type-chars": 145 } as CSSProperties}>
          MediaForge Guard presents the available analysis results, evidence, processing details, and report status so each submission can be reviewed with appropriate context.
        </p>
        <a className="text-link text-link--section type-on-scroll" style={{ "--type-chars": 28 } as CSSProperties} href="/about">About MediaForge Guard <span aria-hidden="true">→</span></a>
      </div>
    </section>
  );
}

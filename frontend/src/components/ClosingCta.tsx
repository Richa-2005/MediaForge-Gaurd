import type { CSSProperties } from "react";
import { Icon } from "./Icon";
import { ReportBlueprintBackdrop } from "./ReportBlueprintBackdrop";

export function ClosingCta() {
  return (
    <section className="closing section" aria-labelledby="closing-title">
      <div className="container">
        <div className="closing-surface scroll-reveal">
          <ReportBlueprintBackdrop />
          <p className="eyebrow type-on-scroll" style={{ "--type-chars": 14 } as CSSProperties}>Ready to begin</p>
          <h2 id="closing-title" className="type-on-scroll type-on-scroll--heading type-on-scroll--center" style={{ "--type-chars": 39 } as CSSProperties}>Start with the media in front of you.</h2>
          <p className="type-on-scroll type-on-scroll--copy type-on-scroll--center" style={{ "--type-chars": 73 } as CSSProperties}>Submit a supported file or public media URL to begin a structured review.</p>
          <div className="closing__actions scroll-reveal">
            <a className="button button--primary" href="/upload">Upload &amp; Analyze <Icon name="arrow" size={17} /></a>
            <div className="closing__secondary-links">
              <a className="text-link" href="/dashboard">Open Dashboard</a>
              <a className="text-link" href="/uploads">View Upload History</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

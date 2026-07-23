import { Icon } from "./Icon";
import { ReportBlueprintBackdrop } from "./ReportBlueprintBackdrop";

export function ClosingCta() {
  return (
    <section className="closing section" aria-labelledby="closing-title">
      <div className="container">
        <div className="closing-surface scroll-reveal">
          <ReportBlueprintBackdrop />
          <p className="eyebrow">Ready to begin</p>
          <h2 id="closing-title">Start with the media in front of you.</h2>
          <p>Submit a supported file or public media URL to begin a structured review.</p>
          <div className="closing__actions">
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

export function InterpretationSection() {
  return (
    <section className="interpretation section" aria-labelledby="interpretation-title">
      <div className="container interpretation__content scroll-reveal">
        <div className="interpretation__label">
          <span aria-hidden="true" />
          <p className="eyebrow">A careful review</p>
        </div>
        <h2 id="interpretation-title">Evidence supports judgment.<br />It does not replace it.</h2>
        <p>
          MediaForge Guard presents the available analysis results, evidence, processing details, and report status so each submission can be reviewed with appropriate context.
        </p>
        <a className="text-link text-link--section" href="/about">About MediaForge Guard <span aria-hidden="true">→</span></a>
      </div>
    </section>
  );
}

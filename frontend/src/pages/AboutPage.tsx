import { ArchitectureDiagram } from "../components/ArchitectureDiagram";
import { InvestigationDoodle } from "../components/InvestigationDoodle";
import { RoadmapTimeline } from "../components/RoadmapTimeline";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { TeamSection } from "../components/TeamSection";
import { TechnologyStack } from "../components/TechnologyStack";

export function AboutPage() {
  return <div className="site-shell case-study-page"><a className="skip-link" href="#main-content">Skip to content</a><SiteHeader /><main id="main-content">
    <section className="case-hero section"><div className="container case-hero__grid"><div className="case-hero__content"><p className="eyebrow reveal">About MediaForge Guard</p><h1 className="reveal reveal--delay-1">A media investigation system built for careful review.</h1><p className="reveal reveal--delay-2">MediaForge Guard brings supported image, video, audio, and text analysis into one traceable investigation record - so the available output can be examined with its context.</p><a className="text-link reveal reveal--delay-3" href="#why-mediaforge">Read the case study <span aria-hidden="true">-&gt;</span></a></div><aside className="case-hero__folio reveal reveal--panel" aria-label="Case study overview"><span>Case study</span><strong>01-09</strong><p>Problem, implemented system, engineering record, and future work.</p></aside></div></section>

    <section className="case-why section" id="why-mediaforge"><div className="container case-why__grid"><div><p className="eyebrow">Why MediaForge Guard?</p><h2>Verification becomes difficult when media, context, and time all move at once.</h2></div><div className="case-why__copy"><p>Misleading media is rarely limited to one format. An image may need visual inspection, a video must be sampled over time, audio needs its own signals, and text calls for claim-oriented analysis.</p><p>Manual review can be slow because the relevant evidence is distributed across specialist methods. MediaForge Guard organizes those implemented paths into one submission record, so AI can assist an investigator's review rather than replace it.</p></div></div></section>

    <section className="case-mission section"><div className="container"><div className="case-mission__lead"><p className="eyebrow">Our vision &amp; mission</p><h2>Trustworthy assistance begins with a readable process.</h2></div><div className="case-mission__columns"><article><span>Vision</span><h3>Support trustworthy, AI-assisted media verification through evidence-aware investigation workflows.</h3><p>Long-term, the project aims to make complex media analysis easier to inspect and understand - without presenting automated output as a substitute for human judgment.</p></article><article><span>Mission</span><h3>Deliver a working system that accepts media, routes it to relevant implemented analysis paths, stores the results, and produces a structured report when available.</h3><p>Today, the product focuses on making its existing processing path legible from upload through review.</p></article></div></div></section>

    <InvestigationDoodle />
    <ArchitectureDiagram />
    <TechnologyStack />
    <TeamSection />
    <RoadmapTimeline />
  </main><SiteFooter /></div>;
}

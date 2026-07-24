import { BrandMark } from "./BrandMark";

const links = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Upload & Analyze", href: "/upload" },
  { label: "Upload History", href: "/uploads" },
  { label: "About MediaForge Guard", href: "/about" },
];

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="container site-footer__top">
        <div className="site-footer__brand">
          <a className="brand" href="/" aria-label="MediaForge Guard home">
            <BrandMark />
            <span>MediaForge Guard</span>
          </a>
          <p>Media authenticity analysis.</p>
        </div>
        <nav className="site-footer__nav" aria-label="Footer navigation">
          {links.map((link) => <a key={link.href} href={link.href} target={link.href.startsWith("http") ? "_blank" : undefined} rel={link.href.startsWith("http") ? "noreferrer" : undefined}>{link.label}</a>)}
        </nav>
      </div>
      <div className="container site-footer__bottom">
        <a className="site-footer__repo" href="https://github.com/Richa-2005/MediaForge-Gaurd/" target="_blank" rel="noreferrer" aria-label="Visit the MediaForge Guard repository">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.7a9.3 9.3 0 0 0-2.9 18.1c.5.1.6-.2.6-.5v-1.8c-2.5.5-3-1.1-3-1.1-.4-1-1-1.3-1-1.3-.8-.5.1-.5.1-.5.9.1 1.4.9 1.4.9.8 1.4 2.1 1 2.6.8.1-.6.3-1 .6-1.2-2-.2-4.1-1-4.1-4.5 0-1 .4-1.8.9-2.4-.1-.2-.4-1.1.1-2.4 0 0 .8-.2 2.5.9a8.5 8.5 0 0 1 4.6 0c1.7-1.1 2.5-.9 2.5-.9.5 1.3.2 2.2.1 2.4.6.6.9 1.4.9 2.4 0 3.5-2.1 4.3-4.1 4.5.3.3.6.9.6 1.8v2.7c0 .3.2.6.6.5A9.3 9.3 0 0 0 12 2.7Z" fill="currentColor" /></svg>
          <span>Visit the repository</span>
          <span aria-hidden="true">-&gt;</span>
        </a>
        <small>© {new Date().getFullYear()} MediaForge Guard</small>
      </div>
    </footer>
  );
}

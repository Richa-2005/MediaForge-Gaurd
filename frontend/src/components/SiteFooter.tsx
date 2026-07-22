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
          {links.map((link) => <a key={link.href} href={link.href}>{link.label}</a>)}
        </nav>
      </div>
      <div className="container site-footer__bottom">
        <small>© {new Date().getFullYear()} MediaForge Guard</small>
      </div>
    </footer>
  );
}

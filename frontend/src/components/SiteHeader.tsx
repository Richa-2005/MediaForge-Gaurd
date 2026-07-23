import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { BrandMark } from "./BrandMark";
import { Icon } from "./Icon";

const links = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Upload History", href: "/uploads" },
  { label: "About", href: "/about" },
];

export function SiteHeader() {
  const { status, user, signOut } = useAuth();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setIsScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className={`site-header ${isScrolled ? "site-header--scrolled" : ""}`}>
      <div className="site-header__inner">
        <a className="brand" href="/" aria-label="MediaForge Guard home" onClick={closeMenu}>
          <BrandMark />
          <span>MediaForge Guard</span>
        </a>

        <nav className="desktop-nav" aria-label="Primary navigation">
          {links.map((link) => (
            <a key={link.href} href={link.href}>{link.label}</a>
          ))}
        </nav>

        <a className="button button--primary header-cta" href="/upload">
          <span>Upload &amp; Analyze</span>
          <Icon name="arrow" size={16} />
        </a>

        <div className="auth-nav">
          {status === "authenticated" ? (
            <>
              <span>{user?.full_name || user?.email}</span>
              <button className="quiet-button" type="button" onClick={signOut}>Sign out</button>
            </>
          ) : (
            <>
              <a href="/login">Sign in</a>
              <a href="/register">Register</a>
            </>
          )}
        </div>

        <button
          className="menu-button"
          type="button"
          aria-label={isMenuOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={isMenuOpen}
          onClick={() => setIsMenuOpen((open) => !open)}
        >
          <Icon name={isMenuOpen ? "close" : "menu"} size={21} />
        </button>
      </div>

      <div className={`mobile-menu ${isMenuOpen ? "mobile-menu--open" : ""}`} aria-hidden={!isMenuOpen}>
        <nav aria-label="Mobile navigation">
          {links.map((link) => (
            <a key={link.href} href={link.href} tabIndex={isMenuOpen ? 0 : -1} onClick={closeMenu}>
              {link.label}
            </a>
          ))}
          <a className="button button--primary" href="/upload" tabIndex={isMenuOpen ? 0 : -1} onClick={closeMenu}>
            Upload &amp; Analyze <Icon name="arrow" size={16} />
          </a>
          {status === "authenticated" ? (
            <button className="quiet-button mobile-auth-action" type="button" tabIndex={isMenuOpen ? 0 : -1} onClick={signOut}>
              Sign out
            </button>
          ) : (
            <div className="mobile-auth-links">
              <a href="/login" tabIndex={isMenuOpen ? 0 : -1} onClick={closeMenu}>Sign in</a>
              <a href="/register" tabIndex={isMenuOpen ? 0 : -1} onClick={closeMenu}>Register</a>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

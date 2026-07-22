import { RecentUploads } from "../components/RecentUploads";
import { SiteFooter } from "../components/SiteFooter";
import { SiteHeader } from "../components/SiteHeader";
import { UploadGuidelines } from "../components/UploadGuidelines";
import { UploadWorkspace } from "../components/UploadWorkspace";

export function UploadPage() {
  return (
    <div className="site-shell upload-page">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <SiteHeader />
      <main id="main-content">
        <section className="upload-page__main section">
          <div className="container upload-page__grid">
            <UploadWorkspace />
            <UploadGuidelines />
          </div>
        </section>
        <section className="upload-page__recent section">
          <div className="container"><RecentUploads /></div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}

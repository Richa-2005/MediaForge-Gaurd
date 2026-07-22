import { Icon } from "./Icon";
import type { CSSProperties } from "react";

const mediaTypes = [
  { name: "Image", description: "Visual analysis", icon: "image" as const },
  { name: "Video", description: "Frame-based review", icon: "video" as const },
  { name: "Audio", description: "Audio analysis", icon: "audio" as const },
  { name: "Text", description: "Text and claim review", icon: "text" as const },
];

export function MediaIntakePanel() {
  return (
    <div className="intake-backdrop reveal reveal--panel">
      <aside className="intake-panel" aria-label="Supported media analysis paths">
        <div className="intake-panel__heading">
          <span className="intake-panel__marker" aria-hidden="true" />
          <span>Media intake</span>
        </div>
        <div className="intake-panel__types">
          {mediaTypes.map((media, index) => (
            <div className="intake-type" key={media.name} style={{ "--item-index": index } as CSSProperties}>
              <span className="intake-type__icon"><Icon name={media.icon} size={19} /></span>
              <span className="intake-type__name">{media.name}</span>
              <span className="intake-type__description">{media.description}</span>
            </div>
          ))}
        </div>
        <p className="intake-panel__note">Structured review begins after submission.</p>
      </aside>
    </div>
  );
}

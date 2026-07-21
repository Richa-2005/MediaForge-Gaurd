import re
from pathlib import Path
from urllib.parse import urlparse

from src.schemas.evidence import Evidence


class SourceAnalyzer:
    """
    Extracts URLs, domains, emails and social media links.
    """

    URL_REGEX = r"https?://[^\s]+"

    EMAIL_REGEX = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    SOCIAL_DOMAINS = {

        "twitter.com",

        "x.com",

        "facebook.com",

        "instagram.com",

        "youtube.com",

        "linkedin.com",

        "reddit.com",

        "t.me",

    }

    def analyze(
        self,
        text: str,
        artifact_path: Path | None = None,
    ) -> Evidence:

        urls = re.findall(
            self.URL_REGEX,
            text,
        )

        emails = re.findall(
            self.EMAIL_REGEX,
            text,
        )

        domains = []

        social_links = []

        for url in urls:

            domain = urlparse(url).netloc.lower()

            domains.append(domain)

            if domain.startswith("www."):

                domain = domain[4:]

            if domain in self.SOCIAL_DOMAINS:

                social_links.append(url)

        unique_domains = sorted(set(domains))

        return Evidence(

            method="Source Extraction",

            score=0.0,

            confidence=1.0,

            summary="Extracted URLs and source information.",

            artifact_path=None,

            metadata={

                "url_count": len(urls),

                "urls": urls,

                "domain_count": len(unique_domains),

                "domains": unique_domains,

                "email_count": len(emails),

                "emails": emails,

                "social_links": social_links,

            },

        )
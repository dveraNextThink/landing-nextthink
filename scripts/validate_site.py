#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate NextThink's generated static site without third-party packages."""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nextthink.es"
SKIP_DIRS = {".git", ".pi-subagents", "plans", "__pycache__"}


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self._in_title = False
        self._in_h1 = False
        self.h1_text: list[str] = []
        self.h1_count = 0
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.anchors: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.scripts: list[str] = []
        self.ids: list[str] = []
        self.schemas: list[str] = []
        self._schema_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = data.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        elif tag == "meta":
            self.metas.append(data)
        elif tag == "link":
            self.links.append(data)
        elif tag == "a":
            self.anchors.append((data.get("href", ""), data.get("aria-label", "")))
        elif tag == "img":
            self.images.append(data)
        elif tag == "script":
            if data.get("type") == "application/ld+json":
                self._schema_buffer = []
            elif data.get("src"):
                self.scripts.append(data["src"])
        if "id" in data:
            self.ids.append(data["id"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script" and self._schema_buffer is not None:
            self.schemas.append("".join(self._schema_buffer))
            self._schema_buffer = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_h1:
            self.h1_text.append(data)
        if self._schema_buffer is not None:
            self._schema_buffer.append(data)

    def meta(self, key: str, value: str) -> str:
        for item in self.metas:
            if item.get(key) == value:
                return item.get("content", "")
        return ""

    def link(self, rel: str) -> str:
        for item in self.links:
            if rel in item.get("rel", "").split():
                return item.get("href", "")
        return ""


def html_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.html")
        if not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)
    )


def url_path_for(file: Path) -> str:
    rel = file.relative_to(ROOT)
    if rel == Path("index.html"):
        return "/"
    if rel.name == "index.html":
        return f"/{rel.parent.as_posix()}/"
    return f"/{rel.as_posix()}"


def local_target(raw: str) -> tuple[Path | None, str]:
    parsed = urlparse(raw)
    if parsed.scheme or raw.startswith("//"):
        if parsed.netloc and parsed.netloc != "nextthink.es":
            return None, parsed.fragment
        path = parsed.path
    else:
        path = parsed.path
    if not path:
        return None, parsed.fragment
    if path == "/":
        return ROOT / "index.html", parsed.fragment
    candidate = ROOT / path.lstrip("/")
    if path.endswith("/"):
        candidate /= "index.html"
    return candidate, parsed.fragment


def parse(file: Path) -> Document:
    parser = Document()
    parser.feed(file.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    errors: list[str] = []
    docs: dict[Path, Document] = {}
    canonicals: set[str] = set()

    for file in html_files():
        doc = parse(file)
        docs[file] = doc
        label = str(file.relative_to(ROOT))
        expected_path = url_path_for(file)
        expected_url = f"{SITE}{expected_path}"

        if doc.lang != "es":
            errors.append(f"{label}: html lang must be es")
        if not 25 <= len(doc.title.strip()) <= 65:
            errors.append(f"{label}: title length is {len(doc.title.strip())}, expected 25-65")
        description = doc.meta("name", "description")
        if not 100 <= len(description) <= 165:
            errors.append(f"{label}: description length is {len(description)}, expected 100-165")
        if doc.h1_count != 1:
            errors.append(f"{label}: expected exactly one h1, found {doc.h1_count}")
        canonical = doc.link("canonical")
        if canonical != expected_url:
            errors.append(f"{label}: canonical {canonical!r} does not match {expected_url!r}")
        if canonical in canonicals:
            errors.append(f"{label}: duplicate canonical {canonical}")
        canonicals.add(canonical)

        required_meta = [
            ("property", "og:title"), ("property", "og:description"),
            ("property", "og:url"), ("property", "og:image"),
            ("name", "twitter:card"), ("name", "twitter:title"),
            ("name", "twitter:description"), ("name", "twitter:image"),
            ("name", "twitter:image:alt"),
        ]
        for key, value in required_meta:
            if not doc.meta(key, value):
                errors.append(f"{label}: missing {value}")
        if doc.meta("property", "og:url") != expected_url:
            errors.append(f"{label}: og:url does not match canonical")

        if len(doc.ids) != len(set(doc.ids)):
            errors.append(f"{label}: duplicate id attribute")
        if not doc.schemas:
            errors.append(f"{label}: missing JSON-LD")
        for index, raw in enumerate(doc.schemas, 1):
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: invalid JSON-LD block {index}: {exc}")

        for image in doc.images:
            src = image.get("src", "")
            if "alt" not in image:
                errors.append(f"{label}: image missing alt: {src}")
            if not image.get("width") or not image.get("height"):
                errors.append(f"{label}: image missing dimensions: {src}")
            target, _ = local_target(src)
            if target and not target.exists():
                errors.append(f"{label}: missing image: {src}")

        for link_data in doc.links:
            rels = set(link_data.get("rel", "").split())
            if not rels.intersection({"stylesheet", "icon", "apple-touch-icon"}):
                continue
            href = link_data.get("href", "")
            target, _ = local_target(href)
            if not href or (target and not target.exists()):
                errors.append(f"{label}: missing linked asset: {href}")

        for src in doc.scripts:
            target, _ = local_target(src)
            if target and not target.exists():
                errors.append(f"{label}: missing script: {src}")

        for meta_key, meta_name in [("property", "og:image"), ("name", "twitter:image")]:
            image_url = doc.meta(meta_key, meta_name)
            target, _ = local_target(image_url)
            if not image_url or (target and not target.exists()):
                errors.append(f"{label}: missing social image: {image_url}")

        for href, _ in doc.anchors:
            if not href:
                errors.append(f"{label}: empty href")
                continue
            if href == "#":
                errors.append(f"{label}: placeholder href=#")
                continue
            if href.startswith(("mailto:", "tel:", "https://wa.me/")):
                continue
            target, fragment = local_target(href)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{label}: broken local link {href}")
                continue
            if fragment:
                target_doc = docs.get(target) or parse(target)
                if fragment not in target_doc.ids:
                    errors.append(f"{label}: missing fragment target {href}")

    sitemap = ROOT / "sitemap.xml"
    try:
        tree = ET.parse(sitemap)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_urls = {node.text or "" for node in tree.findall("sm:url/sm:loc", namespace)}
        indexable_urls = {
            f"{SITE}{url_path_for(file)}" for file, doc in docs.items()
            if "noindex" not in doc.meta("name", "robots")
        }
        if sitemap_urls != indexable_urls:
            missing = sorted(indexable_urls - sitemap_urls)
            extra = sorted(sitemap_urls - indexable_urls)
            if missing:
                errors.append(f"sitemap.xml: missing URLs: {missing}")
            if extra:
                errors.append(f"sitemap.xml: extra URLs: {extra}")
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml: invalid: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {SITE}/sitemap.xml" not in robots:
        errors.append("robots.txt: missing sitemap declaration")

    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: validated {len(docs)} HTML pages, links, assets, metadata, JSON-LD, robots and sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(main())

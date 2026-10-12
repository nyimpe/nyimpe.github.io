#!/usr/bin/env python3
"""Render the Deulme world bible with the existing controlled Markdown renderer.

Run from any directory with Python 3. The downloadable Markdown remains an
unchanged byte-for-byte copy of the source. No third-party packages are needed.
"""

from html import escape
import importlib.util
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/folklore-deulme/world-bible.md"
OUTPUT = ROOT / "posts/korean-folklore-deulme/index.html"
DOWNLOAD = ROOT / "public/downloads/folklore-deulme-bible.md"
TITLE = "들메 — 걸어가는 집들의 시대"
DESCRIPTION = "철마다 찾아오는 서리띠를 피해 집과 마을이 길을 걷는 세계. 움직이는 집의 규칙부터 이주로, 생업, 신앙과 정착을 둘러싼 갈등까지 정리한 독립 설정집."
CANONICAL = "https://nyimpe.github.io/posts/korean-folklore-deulme/"
DOWNLOAD_URL = "/downloads/folklore-deulme-bible.md"


def load_renderer():
    """Load the existing parser without invoking its article entry point."""
    renderer_path = ROOT / "scripts/render-folklore-haedong.py"
    spec = importlib.util.spec_from_file_location("folklore_markdown_renderer", renderer_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load Markdown renderer: {renderer_path}")
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    renderer.TITLE = TITLE
    return renderer


def main():
    renderer = load_renderer()
    source_bytes = SOURCE.read_bytes()
    content, toc = renderer.render_markdown(source_bytes.decode("utf-8"))
    toc_items = []
    for anchor, label in toc:
        label = re.sub(r"^[0-9]+[.)]\s*", "", label)
        toc_items.append(f'<li><a href="#{anchor}">{renderer.inline(label)}</a></li>')
    toc_items = "\n".join(toc_items)
    title = escape(TITLE, quote=True)
    description = escape(DESCRIPTION, quote=True)
    page = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{description}">
    <title>{title} · nyimpe</title>
    <link rel="canonical" href="{CANONICAL}">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{CANONICAL}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/src/style.css">
    <script type="module" src="/src/main.js"></script>
  </head>
  <body>
    <a class="skip-link" href="#content">본문으로 이동</a>
    <header class="site-header">
      <div class="header-content">
        <nav lang="en" class="site-nav" aria-label="Main navigation">
          <a href="/">Home</a>
          <a href="/about/">About</a>
          <a href="https://github.com/nyimpe">GitHub</a>
          <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false" hidden>☾</button>
        </nav>
        <hr>
      </div>
      <img class="site-cat" src="/cat.png" width="88" height="160" alt="주황색과 흰색의 픽셀아트 고양이">
    </header>
    <main id="content">
      <article class="research-post design-post worldbuilding-post">
        <header class="post-header">
          <h1>{title}</h1>
          <time datetime="2026-10-12">2026.10.12</time>
          <p>{description}</p>
          <p class="worldbuilding-download"><a href="{DOWNLOAD_URL}" download>원본 설정집 다운로드 (Markdown)</a></p>
          <p class="image-credit">이 글의 지리·역사·제도와 집이 걷는 규칙은 창작 설정입니다. 전승에서 참고한 소재는 마지막 장에서 구분합니다.</p>
        </header>
        <nav class="post-toc" aria-label="설정집 목차">
          <details open>
            <summary>목차 · {len(toc)}개 장</summary>
            <ol>
{toc_items}
            </ol>
          </details>
        </nav>
{content}
        <aside class="worldbuilding-related" aria-label="함께 읽기">
          <p><strong>함께 읽기</strong></p>
          <ul>
            <li><a href="/posts/korean-folklore-haedong/">해동 — 부적과 마귀의 시대</a></li>
            <li><a href="/posts/korean-folklore-worldbuilding/">해명 — 산신과 왕국의 시대</a></li>
            <li><a href="/posts/korean-folklore-research/">한국 괴물·귀신 항목과 출처</a></li>
          </ul>
          <p><a href="{DOWNLOAD_URL}" download>원본 설정집 다운로드 (Markdown)</a></p>
        </aside>
        <p class="post-back"><a href="/">← Home</a></p>
      </article>
    </main>
    <footer class="site-footer">Small things, made and remade. <a href="https://github.com/nyimpe/nyimpe.github.io">Source code</a></footer>
  </body>
</html>
'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DOWNLOAD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")
    DOWNLOAD.write_bytes(source_bytes)
    print(f"Rendered {len(toc)} sections to {OUTPUT.relative_to(ROOT)}")
    print(f"Copied {len(source_bytes):,} unchanged source bytes to {DOWNLOAD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

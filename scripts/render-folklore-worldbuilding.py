#!/usr/bin/env python3
"""Render the controlled Markdown world bible and copy its unchanged download.

Run from any directory with Python 3. No third-party packages are required.
The source supports headings, paragraphs, flat lists, tables, quotes, fenced
code, links, bold, and inline code. Unknown block syntax fails visibly.
"""

from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/folklore-worldbuilding/world-bible.md"
OUTPUT = ROOT / "posts/korean-folklore-worldbuilding/index.html"
DOWNLOAD = ROOT / "public/downloads/folklore-world-bible.md"
SITE_ORIGIN = "https://nyimpe.github.io"
TITLE = "괴이록 — 한국 괴물·귀신 세계관 설정집"
DESCRIPTION = "한국 괴물·귀신 항목에서 출발한 창작 세계관 설정집. 여울국의 공간, 괴이, 생활, 제도와 공통 법칙을 정리하고 여러 매체에서 확장할 수 있는 기준을 제공합니다."
HEADING = re.compile(r"^(#{1,3})\s+(.+?)(?:\s+\{#([a-z][a-z0-9-]*)\})?$")
LIST = re.compile(r"^(?:(-)|([0-9]+)\.)\s+(.+)$")
INLINE = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\[([^\[\]]+)\]\(([^\s)]+)\)")


def inline(value):
    result = []
    cursor = 0
    for match in INLINE.finditer(value):
        result.append(escape(value[cursor:match.start()]))
        code, bold, label, url = match.groups()
        if code is not None:
            result.append(f"<code>{escape(code)}</code>")
        elif bold is not None:
            result.append(f"<strong>{inline(bold)}</strong>")
        else:
            if not re.match(r"^(?:https?://|/|#)", url):
                raise ValueError(f"Unsupported link target: {url}")
            if url.startswith(SITE_ORIGIN + "/"):
                url = url[len(SITE_ORIGIN):]
            result.append(f'<a href="{escape(url, quote=True)}">{inline(label)}</a>')
        cursor = match.end()
    result.append(escape(value[cursor:]))
    return "".join(result)


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_separator(line):
    return line.startswith("|") and all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in cells(line)
    )


def render_markdown(source):
    lines = source.splitlines()
    if not lines or lines[0] != f"# {TITLE}":
        raise ValueError("Source must begin with the expected article title.")
    content, toc, seen_ids = [], [], set()
    heading_text = TITLE
    section_open = False
    index = 1
    table_count = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            if language and not re.fullmatch(r"[a-z0-9-]+", language):
                raise ValueError(f"Unsupported code language at line {index + 1}")
            block = []
            index += 1
            while index < len(lines) and lines[index] != "```":
                block.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Unclosed code fence")
            class_name = f' class="language-{language}"' if language else ""
            code = escape("\n".join(block))
            content.append(f'<pre tabindex="0" aria-label="{escape(heading_text, quote=True)} 코드"><code{class_name}>{code}</code></pre>')
            index += 1
            continue
        if heading := HEADING.fullmatch(line):
            level = len(heading[1])
            heading_text = heading[2]
            anchor = heading[3]
            if level == 1:
                raise ValueError("Only one H1 is supported")
            if level == 2:
                if not anchor:
                    raise ValueError(f"H2 needs an explicit anchor at line {index + 1}")
                if anchor in seen_ids:
                    raise ValueError(f"Duplicate heading anchor: {anchor}")
                seen_ids.add(anchor)
                if section_open:
                    content.append("</section>")
                content.append(f'<section id="{anchor}" aria-labelledby="{anchor}-title">')
                section_open = True
                content.append(f'<h2 id="{anchor}-title">{inline(heading_text)}</h2>')
                toc.append((anchor, heading_text))
            else:
                if anchor:
                    if anchor in seen_ids:
                        raise ValueError(f"Duplicate heading anchor: {anchor}")
                    seen_ids.add(anchor)
                identifier = f' id="{anchor}"' if anchor else ""
                content.append(f"<h3{identifier}>{inline(heading_text)}</h3>")
            index += 1
            continue
        if line == "---":
            content.append("<hr>")
            index += 1
            continue
        if line.startswith("|"):
            if index + 1 >= len(lines) or not table_separator(lines[index + 1]):
                raise ValueError(f"Table needs a separator at line {index + 1}")
            headers = cells(line)
            table_count += 1
            caption_id = f"world-table-{table_count}"
            content.append(f'<div class="table-scroll" role="region" tabindex="0" aria-labelledby="{caption_id}"><table>')
            content.append(f'<caption id="{caption_id}">{inline(heading_text)}</caption>')
            content.append("<thead><tr>" + "".join(f'<th scope="col">{inline(cell)}</th>' for cell in headers) + "</tr></thead><tbody>")
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                row = cells(lines[index])
                if len(row) != len(headers):
                    raise ValueError(f"Table column mismatch at line {index + 1}")
                content.append("<tr>" + f'<th scope="row">{inline(row[0])}</th>' + "".join(f"<td>{inline(cell)}</td>" for cell in row[1:]) + "</tr>")
                index += 1
            content.append("</tbody></table></div>")
            continue
        if item := LIST.fullmatch(line):
            ordered = item[2] is not None
            tag = "ol" if ordered else "ul"
            start = f' start="{item[2]}"' if ordered and item[2] != "1" else ""
            content.append(f"<{tag}{start}>")
            while index < len(lines) and (item := LIST.fullmatch(lines[index])):
                if (item[2] is not None) != ordered:
                    break
                content.append(f"<li>{inline(item[3])}</li>")
                index += 1
            content.append(f"</{tag}>")
            continue
        if line.startswith(">"):
            quote = []
            while index < len(lines) and lines[index].startswith(">"):
                quote.append(lines[index][1:].lstrip())
                index += 1
            content.append("<blockquote>" + "".join(f"<p>{inline(part)}</p>" for part in "\n".join(quote).split("\n\n") if part.strip()) + "</blockquote>")
            continue
        if line.startswith(("#", "    ", "  -", "<")):
            raise ValueError(f"Unsupported block syntax at line {index + 1}: {line[:60]}")
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            next_line = lines[index]
            if HEADING.fullmatch(next_line) or LIST.fullmatch(next_line) or next_line.startswith(("```", "|", ">")) or next_line == "---":
                break
            if next_line.startswith(("#", "    ", "  -", "<")):
                raise ValueError(f"Unsupported block syntax at line {index + 1}: {next_line[:60]}")
            paragraph.append(next_line)
            index += 1
        content.append(f'<p>{inline(" ".join(paragraph))}</p>')
    if section_open:
        content.append("</section>")
    if not toc:
        raise ValueError("No article sections found")
    return "\n".join(content), toc


def main():
    source_bytes = SOURCE.read_bytes()
    content, toc = render_markdown(source_bytes.decode("utf-8"))
    toc_items = []
    for anchor, label in toc:
        label = re.sub(r"^[0-9]+[.)]\s*", "", label)
        toc_items.append(f'<li><a href="#{anchor}">{inline(label)}</a></li>')
    toc_items = "\n".join(toc_items)
    page = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{DESCRIPTION}">
    <title>{TITLE} · nyimpe</title>
    <link rel="canonical" href="https://nyimpe.github.io/posts/korean-folklore-worldbuilding/">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:title" content="{TITLE}">
    <meta property="og:description" content="{DESCRIPTION}">
    <meta property="og:url" content="https://nyimpe.github.io/posts/korean-folklore-worldbuilding/">
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
          <h1>{TITLE}</h1>
          <time datetime="2026-10-11">2026.10.11</time>
          <p>여울국의 공간·괴이·생활·제도·공통 법칙을 정리한 공용 설정집입니다. 게임·소설·웹툰·TRPG에서 각자의 인물과 이야기를 구성할 수 있도록 세계의 기반과 확장 기준을 제공합니다.</p>
          <p class="worldbuilding-download"><a href="/downloads/folklore-world-bible.md" download>원본 설정집 다운로드 (Markdown)</a></p>
          <p class="image-credit">이 글의 세계·제도·초자연 규칙은 창작 설정입니다. 전승에서 가져온 소재와 새로 정한 해석은 본문에서 구분합니다.</p>
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
            <li><a href="/posts/korean-folklore-research/">한국 괴물·귀신 항목과 출처</a></li>
            <li><a href="/posts/korean-folklore-game-design/">한국 괴물·귀신 게임 기획</a></li>
            <li><a href="/posts/korean-folklore-game-design-50/">한국 괴물·귀신 게임 기획 50선</a></li>
          </ul>
          <p><a href="/downloads/folklore-world-bible.md" download>원본 설정집 다운로드 (Markdown)</a></p>
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

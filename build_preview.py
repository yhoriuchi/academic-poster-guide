"""Render README.md as index.html. Requires Markdown 3.8.2."""

from pathlib import Path

import markdown


root = Path(__file__).resolve().parent
source = (root / "README.md").read_text(encoding="utf-8")
hero, separator, guide = source.partition("\n## Step 1.")
if not separator:
    raise ValueError("Expected the guide to start with a Step 1 heading")

hero_html = markdown.markdown(hero)
badge = (
    '<p><img id="page-views" src="assets/page-views-preview.svg" '
    'width="150" height="20" alt="Page views (local preview)"></p>'
)
hero_html = hero_html.replace("</ul>", f"</ul>\n{badge}", 1)
guide_html = markdown.markdown(
    separator + guide, extensions=["toc", "sane_lists"]
)
for anchor in ("step-1-define-the-message", "step-4-prepare-the-poster-for-printing"):
    if f'id="{anchor}"' not in guide_html:
        raise ValueError(f"Missing section heading for {anchor}")

page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How to Make a Poster</title>
  <link rel="stylesheet" href="assets/github-pages.css">
  <link rel="stylesheet" href="assets/site.css">
  <link rel="stylesheet" href="assets/poster-examples.css">
</head>
<body>
  <div class="container-lg px-3 my-5 markdown-body">
    <main class="page-shell">
      <header class="hero">
{hero_html}
      </header>

      <section aria-labelledby="examples-title">
        <h2 id="examples-title">Two Posters, One Study</h2>
        <p>Click either poster to open the full-size image in a new tab.</p>
        <div class="resource-grid">
          <figure class="resource-card">
            <h3><span aria-hidden="true">❌</span> A Bad but Common Example</h3>
            <a href="assets/poster-typical.png" target="_blank" rel="noopener">
              <img src="assets/poster-typical-thumb.webp" width="720" height="480"
                   alt="Open the full-size text-heavy poster">
            </a>
          </figure>
          <figure class="resource-card">
            <h3><span aria-hidden="true">✔️</span> A Better Poster</h3>
            <a href="assets/poster-better.png" target="_blank" rel="noopener">
              <img src="assets/poster-better-thumb.webp" width="720" height="480"
                   alt="Open the full-size figure-first poster">
            </a>
          </figure>
        </div>
        <p>These examples are based on
          <a href="https://horiuchi.org/research/hp-0107-reassessing-gendered-reactions-to-terrorist-attacks-slumps-or-bumps/">Horiuchi and Johnson (2026)</a>.
          See also the <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4793367">SSRN draft</a>. The adapted figure is licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
      </section>

      <nav class="steps-grid" aria-label="Guide sections">
        <article class="step-card">
          <div class="step-number">Steps 1–3</div>
          <h2>Design the Poster</h2>
          <p>Define your message, lay out the poster, and make the main comparison clear.</p>
          <a class="button button-primary" href="#step-1-define-the-message">Start Designing</a>
        </article>
        <article class="step-card">
          <div class="step-number">Steps 4–5</div>
          <h2>Print and Present</h2>
          <p>Check the final PDF and rehearse your short explanation.</p>
          <a class="button button-primary" href="#step-4-prepare-the-poster-for-printing">Prepare for the Session</a>
        </article>
      </nav>

{guide_html}
    </main>
  </div>
  <script>
    if (location.hostname === "yhoriuchi.github.io" &&
        /^\\/academic-poster-guide\\/(?:index[.]html)?$/.test(location.pathname)) {{
      const badge = document.getElementById("page-views");
      badge.alt = "Page views";
      badge.removeAttribute("width");
      badge.src = "https://hits.sh/yhoriuchi.github.io/academic-poster-guide.svg?label=page%20views";
    }}
  </script>
</body>
</html>
"""
(root / "index.html").write_text(page, encoding="utf-8")

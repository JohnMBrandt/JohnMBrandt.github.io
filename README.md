# johnbrandt.org

Personal site of John Brandt, built with Jekyll on GitHub Pages using the
[Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) theme (pulled in with `remote_theme`, pinned in `_config.yml`).

## Where things live

- `_pages/`: home (`splash-page.md`), About, Publications, Projects and Blog archives
- `_data/publications.yml`: the publication list (rendered by `_includes/pub-item.html`)
- `_portfolio/`, `_blog/`: project pages and archived blog posts
- `_includes/`: the few theme overrides (`feature_row`, `footer.html`, `head/custom.html`, `author-profile-custom-links.html`) plus HTML embeds used by older project pages
- `assets/css/main.scss`: site-specific styles on top of the theme
- `_tools/site-images/`: scripts that regenerate the home banner and project images (not published)

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

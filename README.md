# provandal.dev

Personal site for Erik Smith. Built with Astro, Tailwind, and MDX. Deployed
to GitHub Pages at `provandal.dev`.

## Local development

```bash
npm install
npm run dev
```

The dev server runs at `http://localhost:4321`.

## Commands

| Command | What it does |
| --- | --- |
| `npm install` | Install dependencies |
| `npm run dev` | Start the dev server |
| `npm run build` | Build the production site to `./dist/` |
| `npm run preview` | Preview the built site locally |

## Structure

```
src/
  content/
    writing/          # Blog posts as .mdx files (frontmatter + content)
    projects.ts       # Project data, single source of truth
    config.ts         # Content collection schema
  layouts/
    Base.astro        # Page shell, loaded on every page
  components/
    Nav.astro
    Footer.astro
  pages/
    index.astro       # Landing
    about/index.astro
    projects/index.astro
    writing/
      index.astro     # Writing index
      [...slug].astro # Individual post route
    rss.xml.js        # RSS feed
  styles/
    global.css        # Tailwind base + custom prose
public/
  favicon.svg
  CNAME               # Tells GitHub Pages to serve provandal.dev
```

## Adding a new blog post

Create a new `.mdx` file in `src/content/writing/`. The filename becomes the
slug. Required frontmatter:

```mdx
---
title: "Your title"
description: "One sentence description, shows up under the title and in RSS."
pubDate: 2026-05-01
tags: ["tag-one", "tag-two"]
---

Post content in Markdown or MDX. Embed React components, HTML, whatever.
```

Optional frontmatter fields: `updatedDate`, `draft` (set to `true` to hide
it from the index and RSS while you work on it).

## Adding or editing a project

Edit `src/content/projects.ts`. The array order is the display order. The
first three items show on the landing page.

## Deployment

Pushes to `main` trigger the GitHub Actions workflow in `.github/workflows/deploy.yml`,
which builds the site and deploys to GitHub Pages automatically. Do not commit
the `dist/` directory; it is gitignored and built fresh on every deploy.

### One-time GitHub Pages setup

1. Create a GitHub repository named `provandal.github.io` under the `provandal` account.
2. Push this directory to it.
3. In the repository settings, go to `Pages` and set the source to `GitHub Actions`.
4. The first push to `main` will trigger a deploy.

### One-time DNS setup for provandal.dev

At your domain registrar, add these DNS records:

**A records** (apex domain, all four pointing at GitHub Pages):

```
@  A  185.199.108.153
@  A  185.199.109.153
@  A  185.199.110.153
@  A  185.199.111.153
```

**CNAME record** (for the www subdomain):

```
www  CNAME  provandal.github.io
```

In the GitHub repository under `Settings -> Pages`, set the custom domain to
`provandal.dev` and enable `Enforce HTTPS` once the certificate provisions
(usually within an hour of DNS propagating).

The `public/CNAME` file in this repo tells GitHub Pages which domain to serve,
so you do not need to set it manually every time a deploy runs.

## Design notes

This is deliberate, not accidental. If you are going to modify the look:

- **Type**: Fraunces (display serif, variable with opsz and SOFT axes), Geist
  (body sans), JetBrains Mono (code). Loaded from Google Fonts.
- **Color**: Warm off-black background (`ink-900`) and warm off-white text
  (`ink-100` / `ink-200`). Single signal accent is a muted terracotta
  (`signal`). No pure black, no pure white, no blue, no purple.
- **Aesthetic intent**: editorial-engineer. A well-designed technical journal,
  not a terminal emulator and not a SaaS landing page.

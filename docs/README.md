# Smactu docs

Source for the Smactu documentation site, built with
[Starlight](https://starlight.astro.build) and deployed to GitHub Pages when
changes to `docs/` merge to `main`. Pull requests are built in CI, and a broken
internal link fails the check.

This repository is public. So is everything in this folder, including drafts in
open pull requests.

## Where pages go

Every page is a Markdown file under `src/content/docs/`. The file path becomes
the URL, and the folder decides the sidebar section:

| Folder                              | Sidebar section | For                                              |
| ----------------------------------- | --------------- | ------------------------------------------------ |
| `getting-started/`                  | Getting started | Install, activation, first steps                 |
| `guides/`                           | Guides          | Task-focused how-tos ("Import a project", …)     |
| `reference/`                        | Reference       | Commands, settings, lint rules, error messages   |
| `support.md`                        | Support         | Already written                                  |
| `index.mdx`                         | Home page       | Update the cards as major guides land            |

A section appears in the sidebar once its folder contains a page. To add a new
section, add it to `sections` in `astro.config.mjs`. Use subfolders inside a
section for nested groups.

File names are lowercase and hyphenated: `guides/import-a-project.md` is served
at `/guides/import-a-project/`.

## Front matter

Start every page with:

```markdown
---
title: Import a Sysmac Studio project
description: One sentence shown in search results and link previews.
sidebar:
  order: 1 # position within its section; lower comes first
---
```

`title` becomes the page heading, so don't repeat it as a `#` heading in the
body. Start body sections at `##`.

## Writing rules

- **Links between pages** are root-relative with a trailing slash and no file
  extension: `[Install Smactu](/getting-started/install/)`. Don't add
  `/smactu-releases/`, because the build adds the base path. Links to headings
  work too: `/reference/settings/#smactu-lint-enabled`. Relative links
  (`../install/`) are rejected by the link check.
- **Images** go in `src/assets/` and are referenced relatively from the page,
  e.g. `![Smactu import dialog](../../../assets/import-dialog.png)`. Always
  write alt text. Crop to the relevant UI, and never show customer project
  names, licence keys or file paths that identify a customer.
- **Callouts:** `:::note`, `:::tip`, `:::caution`, `:::danger`, closed with
  `:::`. Add a custom title with `:::caution[Back up first]`.
- **UI labels** are bold and match the UI exactly: **Install from VSIX…**.
  Commands and file names go in backticks.
- Spelling is Australian English (licence, organise, colour). The product names
  are Smactu, VS Code, Sysmac Studio and Omron.
- Write for the **latest stable release**. Merge docs for a new feature when it
  ships stable, not when it reaches prerelease.

## Keep out of the docs

The docs say how to use Smactu, not how it works inside. Leave out:

- how licensing, activation or licence checks work internally;
- native components, internal file formats or protocols, and debug or hidden
  settings;
- licence keys, tokens, credentials and internal URLs;
- customer projects, names or screenshots that show them.

If in doubt, leave it out and ask in the pull request.

## Preview locally

Requires Node.js 22.23 or later.

```bash
cd docs
npm ci
npm run dev     # http://localhost:4321/smactu-releases/ with live reload
npm run build   # what CI runs; reports broken links
```

Restart `npm run dev` after creating a new section folder so the sidebar picks
it up.

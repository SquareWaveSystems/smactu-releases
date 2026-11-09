// @ts-check
import { existsSync, readdirSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import remarkBaseLinks from './src/plugins/remark-base-links.mjs';

// Served from GitHub Pages at /smactu-releases/ until a custom domain is set.
// When it is: set `site` to the new origin, set `base` to '/', and add
// public/CNAME. Page content does not need to change (see remark-base-links).
const site = 'https://squarewavesystems.github.io';
const base = '/smactu-releases';

// Sidebar sections, one per folder in src/content/docs/. A section appears once
// its folder contains a page, and lists pages ordered by `sidebar.order`.
const sections = [
  ['Getting started', 'getting-started'],
  ['Guides', 'guides'],
  ['Reference', 'reference'],
];
const hasPages = (directory) => {
  const path = new URL(`./src/content/docs/${directory}/`, import.meta.url);
  return existsSync(path) && readdirSync(path, { recursive: true }).some((f) => /\.mdx?$/.test(String(f)));
};

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  markdown: {
    processor: unified({ remarkPlugins: [[remarkBaseLinks, { base }]] }),
  },
  integrations: [
    starlight({
      title: 'Smactu',
      description: 'Documentation for Smactu, the VS Code extension for Omron Sysmac Studio projects.',
      logo: { src: './src/assets/smactu-logo.png', alt: 'Smactu logo' },
      favicon: '/favicon.png',
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/SquareWaveSystems/smactu-releases' },
      ],
      editLink: {
        baseUrl: 'https://github.com/SquareWaveSystems/smactu-releases/edit/main/docs/',
      },
      lastUpdated: true,
      routeMiddleware: './src/route-data.ts',
      plugins: [starlightLinksValidator()],
      sidebar: [
        ...sections
          .filter(([, directory]) => hasPages(directory))
          .map(([label, directory]) => ({ label, items: [{ autogenerate: { directory } }] })),
        { label: 'Support', slug: 'support' },
      ],
    }),
  ],
});

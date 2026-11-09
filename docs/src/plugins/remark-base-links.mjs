// Prefix the site base path onto root-relative links, so pages can link to
// `/getting-started/install/` and keep working whether the site is served from
// a GitHub Pages project path (/smactu-releases/) or from a custom domain.
//
// Covers Markdown links and definitions, `href`/`link` string props on MDX
// components (e.g. <LinkCard href="/support/" />) and splash-page hero actions.
import { visit } from 'unist-util-visit';

export default function remarkBaseLinks({ base = '/' } = {}) {
  const prefix = base.replace(/\/$/, '');
  const withBase = (url) => {
    if (typeof url !== 'string' || !url.startsWith('/') || url.startsWith('//')) return url;
    if (url === prefix || url.startsWith(`${prefix}/`)) return url;
    return `${prefix}${url}`;
  };

  return (tree, file) => {
    if (!prefix) return;

    visit(tree, ['link', 'definition'], (node) => {
      node.url = withBase(node.url);
    });

    visit(tree, ['mdxJsxFlowElement', 'mdxJsxTextElement'], (node) => {
      for (const attribute of node.attributes ?? []) {
        if (attribute.type === 'mdxJsxAttribute' && ['href', 'link'].includes(attribute.name)) {
          attribute.value = withBase(attribute.value);
        }
      }
    });

    const actions = file.data?.astro?.frontmatter?.hero?.actions;
    if (Array.isArray(actions)) {
      for (const action of actions) action.link = withBase(action.link);
    }
  };
}

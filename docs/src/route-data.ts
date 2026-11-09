import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// Hero actions on splash pages are read from frontmatter at render time, so the
// remark base-link plugin can't reach them. Prefix the base path here instead,
// letting pages use root-relative links like `/getting-started/install/`.
export const onRequest = defineRouteMiddleware((context) => {
  const prefix = import.meta.env.BASE_URL.replace(/\/$/, '');
  const actions = context.locals.starlightRoute.entry.data.hero?.actions;
  if (!prefix || !actions) return;
  for (const action of actions) {
    const { link } = action;
    if (link.startsWith('/') && !link.startsWith('//') && link !== prefix && !link.startsWith(`${prefix}/`)) {
      action.link = `${prefix}${link}`;
    }
  }
});

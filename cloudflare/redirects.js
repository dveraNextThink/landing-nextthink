const CANONICAL_HOST = "nextthink.es";

export default {
  async fetch(request) {
    const url = new URL(request.url);

    let shouldRedirect = false;

    if (url.protocol !== "https:") {
      url.protocol = "https:";
      shouldRedirect = true;
    }

    if (url.hostname === `www.${CANONICAL_HOST}`) {
      url.hostname = CANONICAL_HOST;
      shouldRedirect = true;
    }

    if (url.hostname === CANONICAL_HOST && url.pathname.endsWith("/index.html")) {
      url.pathname = url.pathname.slice(0, -"index.html".length);
      shouldRedirect = true;
    }

    if (shouldRedirect) {
      return Response.redirect(url.toString(), 301);
    }

    return fetch(request);
  },
};

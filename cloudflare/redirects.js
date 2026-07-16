const CANONICAL_HOST = "nextthink.es";

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.hostname === `www.${CANONICAL_HOST}`) {
      url.protocol = "https:";
      url.hostname = CANONICAL_HOST;
      return Response.redirect(url.toString(), 301);
    }

    if (url.hostname === CANONICAL_HOST && url.pathname === "/index.html") {
      url.protocol = "https:";
      url.pathname = "/";
      return Response.redirect(url.toString(), 301);
    }

    return fetch(request);
  },
};

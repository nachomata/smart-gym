import type { APIRoute } from "astro";

export const GET: APIRoute = async ({ params, request }) => {
  const response = new Response(null, { status: 302 });
  response.headers.set("Location", "/");
  response.headers.set("Set-Cookie", "user=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0");
  return response;
}
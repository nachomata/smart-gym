import { API_URL } from "../../consts/consts";
import type { APIRoute } from "astro";

export const POST: APIRoute = async ({ params, request }) => {
  const { user, password } = await request.json();
  const response = await fetch(`${API_URL}/api/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user, password }),
  });
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return new Response(
      JSON.stringify({
        success: true,
        user: data.name,
      })
    );
  }

  return new Response(
    JSON.stringify({
      success: false,
    })
  );
};

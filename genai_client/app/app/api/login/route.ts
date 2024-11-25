import { cookies } from "next/headers";
import { headerAccess } from "../../_utils/cookie";

export async function POST(req: Request) {
  try {
    const cookieStore = await cookies();
    const data = await req.json();
    const res = await fetch(`${process.env.USER_SERIVCE}/api/v1/login`, {
      cache: "no-cache",
      headers: { "Content-Type": "application/json" },
      method: "post",
      body: JSON.stringify(data),
    });

    if (res.ok) {
      const oneDay = 24 * 60 * 60 * 1000;
      cookieStore.set({
        name: "access",
        value: headerAccess(res.headers),
        httpOnly: true,
        expires: Date.now() + oneDay,
        path: "/",
      });
      return Response.json(await res.json(), { status: 200 });
    }
  } catch (error) {
    console.error(error);
  }
  return Response.json("error", { status: 403 });
}

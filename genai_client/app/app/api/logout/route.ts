import { cookies } from "next/headers";

export async function GET() {
  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";

    if (!access) {
      return Response.json("error", { status: 403 });
    }

    const res = await fetch(`${process.env.USER_SERIVCE}/api/v1/logout`, {
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
        Cookie: `access=${access}`,
      },
      method: "get",
    });

    if ([401, 200].includes(res.status)) {
      cookieStore.delete("access");
      return Response.json("logged out", {
        status: 200,
        headers: { Cookie: "access=" },
      });
    }
  } catch (error) {
    console.error(error);
  }
  return Response.json("error", { status: 403 });
}

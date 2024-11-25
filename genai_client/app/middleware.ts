import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

import { getUser } from "./app/_utils/fetch/user";
import { headerAccess } from "./app/_utils/cookie";

export async function middleware(request: NextRequest) {
  const unauthorizedResponse = NextResponse.redirect(
    new URL("/auth", request.url)
  );

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    if (!access.trim()) {
      return unauthorizedResponse;
    }
    const userResponse = await getUser(access);

    if (userResponse.ok) {
      const response = NextResponse.next();
      const user = await userResponse.json();

      response.headers.set("x-uid", user.id);
      response.cookies.set({
        name: "access",
        value: headerAccess(userResponse.headers),
        maxAge: 24 * 60 * 60,
        httpOnly: true,
      });
      return response;
    }
  } catch (error) {
    console.error(error);
  }
  return unauthorizedResponse;
}

export const config = {
  matcher: ["/", "/api/account/:path*"],
};

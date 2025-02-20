import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

import { getUser } from "./app/_utils/fetch/user";
import { headerAccess } from "./app/_utils/cookie";

export async function middleware(request: NextRequest) {  
  const cookieStore = await cookies();
  try {
    const access = cookieStore.get("access")?.value ?? "";

    if (!access.trim()) {
      return NextResponse.redirect(
        new URL("/auth", request.url)
      );
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

  cookieStore.delete("access")
  return NextResponse.redirect(
    new URL("/auth/logout", request.url)
  );
}

export const config = {
  matcher: ["/", "/scraper", "/api/account/:path*"],
};

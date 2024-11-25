import { NextResponse } from "next/server";
import { headerAccess } from "../../_utils/cookie";

export async function GET(req: Request, res: Response) {
  try {
    const userResponse = await fetch(
      `${process.env.USER_SERIVCE}/api/v1/user`,
      {
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
          Cookie: `access=${headerAccess(req.headers)}`,
        },
        method: "get",
      },
    );

    if (userResponse.ok) {
      return NextResponse.json(await userResponse.json())
    }
  } catch (error) {
    console.error(error);
  }

  return Response.json("error", { status: 403 });
}

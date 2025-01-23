import { NextResponse } from "next/server";
import { headerAccess } from "../../_utils/cookie";

export async function GET(req: Request, res: Response) {
  try {
    const projectResponse = await fetch(
      `${process.env.GENAI_SERIVCE}/api/v1/project`,
      {
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
          Cookie: `access=${headerAccess(req.headers)}`,
        },
        method: "get",
      },
    );
    
    
    if (projectResponse.ok) {
      return NextResponse.json(await projectResponse.json())
    }
  } catch (error) {
    console.error(error);
  }

  return Response.json("error", { status: 403 });
}

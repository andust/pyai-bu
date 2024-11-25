"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";

export async function createChat() {
  const cookieStore = await cookies();
  let newChatId = "";
  try {
    const res = await fetch(`${process.env.GENAI_SERIVCE}/api/v1/chat`, {
      cache: "no-cache",
      headers: {
        Cookie: `access=${cookieStore.get("access")?.value}`,
      },
      method: "post",
    });
    if (res.ok) {
      const newChat = await res.json();
      newChatId = newChat.id;
    }
  } catch (error) {
    console.log(error);
  }
  redirect(`/chat/${newChatId}`);
}

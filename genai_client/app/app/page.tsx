import { cookies } from "next/headers";
import Link from "next/link";

import { Chat } from "./_models/chat";
import { createChat } from "./actions";
import { getChats } from "./_utils/fetch/chat";
import Button from "./_atoms/button/Button";
import MainLayout from "./_layout/MainLayout";

export default async function Home() {
  let chats: Chat[] = [];
  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getChats(access);
    if (res.ok) {
      chats = await res.json();
    }
  } catch (error) {
    console.log(error);
  }

  return (
    <MainLayout>
      <form className="mb-12" action={createChat}>
        <Button type="submit">New chat</Button>
      </form>
      <div className="flex flex-col space-y-3">
        {chats.map(({ id, questions }) => (
          <Link
            className="space-y-5 bg-slate-900 rounded p-2"
            key={id}
            href={`/chat/${id}`}
          >
            {Array.isArray(questions)
              ? questions[questions.length - 1].content
              : "New chat"}
          </Link>
        ))}
      </div>
    </MainLayout>
  );
}

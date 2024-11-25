import { IdParams } from "@/app/types";
import ChatContent from "@/app/_molecules/chat/ChatContent";
import ChatForm from "@/app/_molecules/chat/ChatForm";
import MainLayout from "@/app/_layout/MainLayout";

// TODO select how ask chat - rag or normal question
export default async function New({ params }: IdParams) {
  const chatId = (await params).id || "";
  return (
    <MainLayout>
      <ChatContent id={chatId} />
      <hr className="my-10" />
      <ChatForm id={chatId} />
    </MainLayout>
  );
}

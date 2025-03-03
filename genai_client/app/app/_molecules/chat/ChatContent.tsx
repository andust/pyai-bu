"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";

import { ChatI, getClientChat, removeClientChat } from "@/app/_models/chat";
import { ChatContext } from "@/app/_context/chatContext";
import Button from "@/app/_atoms/button/Button";
import Confirm from "@/app/_atoms/confirm/Confirm";

const ChatContent = ({ id }: { id: string }) => {
  const router = useRouter();
  const { questions, setQuestions } = useContext(ChatContext);
  useEffect(() => {
    getClientChat(id)
      .then((res) => {
        return res.json();
      })
      .then((chat: ChatI) => {
        setQuestions(chat.questions);
      });
  }, [id, setQuestions]);

  const handleOnDelete = () => {
    removeClientChat(id).then((res) => {
      if (res.ok) {
        router.push("/");
      }
    });
  };

  return (
    <div className="space-y-8">
      <Confirm onConfirm={handleOnDelete}>
        <Button>Delete chat</Button>
      </Confirm>

      {questions?.map((question, index) => (
        <div key={`${question.content}-${index}`} className="mb-4">
          <h2 className="p-4 rounded bg-slate-700 text-white mb-2">
            {question.content}
          </h2>
          <pre
            className={`p-4 text-left w-full bg-slate-900 rounded shadow-inner overflow-auto text-white whitespace-pre-wrap`}
          >
            {question.answer}
          </pre>
        </div>
      ))}
    </div>
  );
};

export default ChatContent;

"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";

import { Chat, getClientChat, removeClientChat } from "@/app/_models/chat";
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
      .then((chat: Chat) => {
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

      {questions?.map((question, index) => {
        const whitespaceClassname = question.answer.includes("```")
          ? "whitespace-pre"
          : "whitespace-pre-line";

        return (
          <div key={`${question.content}-${index}`}>
            <h2 className="p-2 rounded bg-slate-700 mb-1">
              {question.content}
            </h2>
            <pre
              className={`p-2 ${whitespaceClassname} text-left w-11/12 bg-slate-900 rounded ml-auto mr-0 overflow-auto `}
            >
              {question.answer}
            </pre>
          </div>
        );
      })}
    </div>
  );
};

export default ChatContent;

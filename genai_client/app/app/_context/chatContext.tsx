"use client";
import { createContext, useState } from "react";

import { ChildrenProp } from "../types";
import { Question } from "../_models/chat";

interface ChatContextProps {
  questions: Question[];
  setQuestions: (questions: Question[]) => void;
}

export const ChatContext = createContext<ChatContextProps>({
  questions: [],
  setQuestions: () => {},
});

export const ChatProvider = ({ children }: ChildrenProp) => {
  const [questions, setQuestions] = useState<Question[]>([
    {
      content: "",
      answer: "",
    },
  ]);

  return (
    <ChatContext.Provider value={{ questions, setQuestions }}>
      {children}
    </ChatContext.Provider>
  );
};

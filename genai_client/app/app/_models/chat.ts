import { QuestionType } from "../types";

export interface ChatI {
  id: string;
  title?: string;
  questions: Question[];
}

export class Chat {
  chat: ChatI;

  constructor(chat: ChatI) {
    this.chat = chat;
  }
  
  public get title(): string {
    if (this.chat.title && this.chat.title !== "") {
      return this.chat.title;
    }
  
    return Array.isArray(this.chat.questions)
      ? this.chat.questions[this.chat.questions.length - 1]?.content
      : "New chat";
  }
}

export interface Question {
  content: string;
  answer: string;
}

export const getClientChat = async (id: string) => {
  return fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/chat/${id}`, {
    cache: "no-cache",
    credentials: "include",
    method: "get",
  });
};

export const getClientAskChat = async (
  id: string,
  question: string,
  questionType: QuestionType,
  documentId: string
) => {
  return fetch(
    `${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/rag/ask/${id}`,
    {
      cache: "no-cache",
      credentials: "include",
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        question_type: questionType,
        document_id: documentId,
      }),
    }
  );
};

export const removeClientChat = async (id: string) => {
  return fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/chat/${id}`, {
    cache: "no-cache",
    credentials: "include",
    method: "delete",
  });
};

export interface Chat {
  id: string;
  user_id: string;
  questions: Question[] | null;
}

export interface Question {
  content: string;
  answer: string;
  context: "chat" | "rag";
}

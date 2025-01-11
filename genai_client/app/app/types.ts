import { ReactNode } from "react";

export interface FilterResponse<T> {
  results: T[];
}

export type Children = JSX.Element | ReactNode | string;

export interface ChildrenProp {
  children: Children;
}
export interface ClassNameProp {
  className?: string;
}

export interface IdParams {
  params: Promise<{ id: string }>;
}

export type QuestionType = "chat" | "rag";

export interface SearchParams {
  searchParams: { [key: string]: string | string[] | undefined }
} 
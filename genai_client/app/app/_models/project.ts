import { ComplexityLevel } from "../types";

export interface Project {
  id?: string;
  title: string;
  description: string;
  complexity: ComplexityLevel;
}

export const getClientFiles = async () => {
  return fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/file/`, {
    cache: "no-cache",
    credentials: "include",
    method: "get",
  });
};
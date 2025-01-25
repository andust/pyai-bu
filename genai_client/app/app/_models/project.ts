import { ComplexityLevel } from "../types";
import { Estimation } from "./restimation";

export interface Project {
  id?: string;
  title: string;
  description: string;
  complexity: ComplexityLevel;
  estimation?: Estimation;
}

export const getClientFiles = async () => {
  return fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/file/`, {
    cache: "no-cache",
    credentials: "include",
    method: "get",
  });
};

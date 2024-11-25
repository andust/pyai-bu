export interface DocFile {
  id: string;
  filename: string;
  upload_date: string;
}

export const getClientFiles = async () => {
  return fetch(`${process.env.NEXT_PUBLIC_GENIA_SERIVCE}/api/v1/file/`, {
    cache: "no-cache",
    credentials: "include",
    method: "get",
  });
};
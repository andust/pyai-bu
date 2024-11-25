export const getChats = async (access: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/chat`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

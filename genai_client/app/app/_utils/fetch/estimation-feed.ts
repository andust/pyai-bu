export const getEstimationFeeds = async (access: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/estimation-feed`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

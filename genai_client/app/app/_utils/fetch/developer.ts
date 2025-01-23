export const getDevelopers = async (access: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/developer`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

export const getDeveloper = async (access: string, developerId: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/developer/${developerId}`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

export const getProjects = async (access: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/project`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

export const getProject = async (access: string, projectId: string) => {
  return fetch(`${process.env.GENAI_SERIVCE}/api/v1/project/${projectId}`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

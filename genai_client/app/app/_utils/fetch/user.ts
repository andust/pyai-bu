export const getUser = async (access: string) => {
  return fetch(`${process.env.USER_SERIVCE}/api/v1/user`, {
    cache: "no-cache",
    headers: {
      Cookie: `access=${access}`,
    },
    credentials: "include",
    method: "get",
  });
};

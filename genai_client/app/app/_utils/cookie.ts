export const headerAccess = (headers: Headers): string => {
  const cookies = headers.getSetCookie();
  for (let index = 0; index < cookies.length; index++) {
    const value = cookies[index];
    const [k, v] = value.split("=");
    if (k === "access") {
      return v.split("; Path")[0];
    }
  }

  return "";
};

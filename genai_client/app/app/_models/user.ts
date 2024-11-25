export interface User {
  id: string;
  username: string;
  email: string;
  role: "client" | "admin" | "super-admin";
  createdAt: string;
  updatedAt: string;
}

export const getClientUser = async () => {
  return fetch("/api/account", { method: "get", cache: "no-cache" });
};

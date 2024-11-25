export interface User {
  id: string;
  username: string;
  email: string;
  role: "client" | "admin" | "super-admin";
  createdAt: string;
  updatedAt: string;
}

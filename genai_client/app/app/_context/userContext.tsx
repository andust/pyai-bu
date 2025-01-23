"use client";
import { createContext, useContext, useEffect, useState } from "react";

import { getClientUser, User } from "../_models/user";
import { ChildrenProp } from "../types";

interface UserContextProps {
  user?: User;
  setUser: (user: User) => void;
  logOut: () => Promise<void>;
}

export const UserContext = createContext<UserContextProps>({
  user: undefined,
  setUser: () => {},
  logOut: async () => {},
});

export const UserProvider = ({ children }: ChildrenProp) => {
  const [user, setUser] = useState<User>();

  const logOut = async () => {
    try {
      const res = await fetch("/api/logout", {
        cache: "no-cache",
        method: "get",
      });
      if (res.ok) {
        setUser(undefined);
        window.location.href = "/";
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <UserContext.Provider value={{ user, setUser, logOut }}>
      {children}
    </UserContext.Provider>
  );
};

export const LoadUser = ({ children }: ChildrenProp) => {
  const { setUser } = useContext(UserContext);

  useEffect(() => {
    getClientUser().then(async (result) => {
      if (result.ok) {
        setUser(await result.json());
      }
    });
  }, []);

  return children;
};

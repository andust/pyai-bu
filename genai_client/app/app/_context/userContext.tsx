"use client";
import { createContext, useContext, useEffect, useState } from "react";

import { getClientUser, User } from "../_models/user";
import { ChildrenProp } from "../types";

interface UserContextProps {
  user?: User;
  setUser: (user: User) => void;
}

export const UserContext = createContext<UserContextProps>({
  user: undefined,
  setUser: () => {},
});

export const UserProvider = ({ children }: ChildrenProp) => {
  const [user, setUser] = useState<User>();

  return (
    <UserContext.Provider value={{ user, setUser }}>
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

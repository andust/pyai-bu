"use client";

import { ChatProvider } from "./_context/chatContext";
import { UserProvider } from "./_context/userContext";
import { ChildrenProp } from "./types";

export default function Providers({ children }: ChildrenProp) {
  return (
    <UserProvider>
      <ChatProvider>
        {children}
      </ChatProvider>
    </UserProvider>
  );
}

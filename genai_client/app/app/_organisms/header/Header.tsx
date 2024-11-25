"use client";

import { useContext } from "react";
import { UserContext } from "@/app/_context/userContext";
import LogoutButton from "@/app/_molecules/logout-button/LogoutButton";
import Link from "next/link";

export default function Header() {
  const { user } = useContext(UserContext);

  return (
    <header className="flex justify-between items-center container">
      <div className="flex gap-x-5">
        <Link href="/">Home</Link>
        <Link href="/files">Files</Link>
        <Link href="/images">Images</Link>
      </div>
      <div className="gap-x-2">
        User: {user?.email}&nbsp;
        <LogoutButton>Logout</LogoutButton>
      </div>
    </header>
  );
}

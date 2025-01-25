"use client";

import { useContext } from "react";
import { UserContext } from "@/app/_context/userContext";
import Link from "next/link";
import Button from "@/app/_atoms/button/Button";

export default function Header() {
  const { user, logOut } = useContext(UserContext);

  const handleLogout = async () => {
    await logOut()
  }


  return (
    <header className="flex justify-between items-center container">
      <div className="flex gap-x-5">
        <Link href="/">Home</Link>
        <Link href="/files">Files</Link>
        <Link href="/images">Images</Link>
        <Link href="/scraper">Scraper</Link>
        <Link href="/newsletter">Newsletter</Link>
        <Link href="/project">Project</Link>
        <Link href="/estimation-feeds">Estimation feeds</Link>
      </div>
      <div className="gap-x-2">
        User: {user?.email}&nbsp;
        {user && (
          <Button onClick={handleLogout}>Logout</Button>
        )}
      </div>
    </header>
  );
}

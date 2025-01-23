"use client";
import type { Metadata } from "next";
import { useContext } from "react";
import Link from "next/link";
import { LoadUser, UserContext } from "../_context/userContext";
import Button from "../_atoms/button/Button";

export const metadata: Metadata = {
  title: "Chat Auth",
  description: "Auth user",
};

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { user, logOut } = useContext(UserContext);
  const handleLogout = async () => {
    await logOut()
  }

  return (
    <LoadUser>
      <div className="space-y-5">
        <header className="py-3">
          <ul className="container flex items-center justify-between">
            <ul className="flex space-x-3">
              <li>
                <Link href="/">Register</Link>
              </li>
            </ul>
            {user && (
              <li>
                <Button onClick={handleLogout}>Logout</Button>
              </li>
            )}
          </ul>
        </header>
        <div className="container">
          <main>{children}</main>
        </div>
      </div>
    </LoadUser>
  );
}

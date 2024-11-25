"use client";
import type { Metadata } from "next";
import Link from "next/link";
import LogoutButton from "../_molecules/logout-button/LogoutButton";
import { LoadUser, UserContext } from "../_context/userContext";
import { useContext } from "react";

export const metadata: Metadata = {
  title: "Chat Auth",
  description: "Auth user",
};

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { user } = useContext(UserContext);
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
                <LogoutButton>Logout</LogoutButton>
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

"use client";

import { useSearchParams } from "next/navigation";
import { useContext, useEffect } from "react";
import { UserContext } from "../../_context/userContext";
import { redirect } from "next/navigation";

export default function Logout() {
  const { user, logOut } = useContext(UserContext);

  useEffect(() => {
    if (user) {
      logOut().then(() => {}).finally(() => {
        redirect("/");
      });
    }
  }, [])

  return null;
}

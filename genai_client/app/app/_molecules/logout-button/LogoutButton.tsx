"use client";

import Button, { ThemeProp } from "../../_atoms/button/Button";
import { ChildrenProp, ClassNameProp } from "../../types";

interface Props extends ChildrenProp, ClassNameProp, ThemeProp {}

export default function LogoutButton({
  children,
  className = "",
  theme = "base",
}: Props) {
  const handleLogout = async () => {
    try {
      const res = await fetch("/api/logout", {
        cache: "no-cache",
        method: "get",
      });
      if (res.ok) {
        window.location.href = "/"
      }
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <Button className={className} theme={theme} onClick={handleLogout}>
      {children}
    </Button>
  );
}

"use client";

import { useContext } from "react";
import AuthLayout from "../_layout/AuthLayout";
import LoginForm from "../_molecules/login-form/LoginForm";
import { UserContext } from "../_context/userContext";
import { redirect } from "next/navigation";

export default function Auth() {
  const { user } = useContext(UserContext);

  if (user?.id) {
    redirect("/");
  }

  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  );
}

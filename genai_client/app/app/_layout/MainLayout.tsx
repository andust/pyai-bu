import type { Metadata } from "next";
import { LoadUser } from "../_context/userContext";
import Header from "../_organisms/header/Header";

export const metadata: Metadata = {
  title: "Chat App",
  description: "Retrieval Augmented Generation",
};

export default async function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <LoadUser>
      <div className="py-3">
        <Header />
        <main className="font-[family-name:var(--font-geist-sans)] container py-12">
          {children}
        </main>
      </div>
    </LoadUser>
  );
}

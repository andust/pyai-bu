"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import Button from "../../_atoms/button/Button";
import { Developer } from "@/app/_models/developer";

interface Props {
  projectId: string;
  developers: Developer[]
}

const EstimationToolForm = ({ projectId, developers }: Props) => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    fetch(
      `${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/estimation/`,
      {
        credentials: "include",
        method: "POST",
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ project_id: projectId }),
      }
    ).then(async (res) => {
      if (res.ok) {
        // router.push("/files");
      }
    });
  };

  return (
    <form className="space-y-6 text-black " onSubmit={onSubmitHandler}>
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading}>
          Estimate project
        </Button>
      </div>
    </form>
  );
};

export default EstimationToolForm;

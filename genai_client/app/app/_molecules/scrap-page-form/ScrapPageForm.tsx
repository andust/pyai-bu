"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { z } from "zod";

import Button from "../../_atoms/button/Button";
import Textarea from "@/app/_atoms/textarea/Textarea";

const urlSchema = z.string().url();

const ScrapePageForm = () => {
  const router = useRouter();

  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);

  const urls = content
    .split(/\r?\n/)
    .map((a) => a.trim())
    .filter((a) => a);
  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (urls.length) {
      fetch(
        `${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/scraper/scrape-pages/`,
        {
          credentials: "include",
          method: "POST",
          cache: "no-cache",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ urls }),
        }
      ).then(async (res) => {
        if (res.ok) {
          router.push("/files");
        }
      });
    }
  };

  useEffect(() => {
    const errorRecord: Record<string, string> = {};
    urls.forEach((url) => {
      try {
        urlSchema.parse(url);
      } catch (e) {
        if (e instanceof z.ZodError) {
          errorRecord[url] = e.errors
            .map((a) => `👉 ${a.message} (${url})`)
            .join("\n");
        }
      }
    });
    setErrors(Object.values(errorRecord));
  }, [content]);

  return (
    <form className="space-y-5 text-black" onSubmit={onSubmitHandler}>
      <p className="text-red small whitespace-pre-line">{errors.join("\n")}</p>
      <label>
        <small className="text-slate-500">Add multiple pages by new line</small>
        <Textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={isLoading}
        />
      </label>
      <div className="flex justify-end">
        <Button type="submit">Scrape</Button>
      </div>
    </form>
  );
};

export default ScrapePageForm;

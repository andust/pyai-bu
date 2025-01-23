"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { z } from "zod";

import Button from "../../_atoms/button/Button";
import Textarea from "@/app/_atoms/textarea/Textarea";
import Input from "@/app/_atoms/input/Input";

const urlSchema = z.string().url();

const NewsletterGeneratorForm = () => {
  const router = useRouter();

  const [sourceUrl, setSourceUrl] = useState("");
  const [questionContext, setQuestionContext] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (errors.length === 0 && sourceUrl) {
      fetch(
        `${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/newsletter/`,
        {
          credentials: "include",
          method: "POST",
          cache: "no-cache",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ urls: [sourceUrl], question_context: questionContext }),
        }
      ).then(async (res) => {
        if (res.ok) {
          // router.push("/files");
        }
      });
    }
  };

  useEffect(() => {
    if (sourceUrl) {
      const errorRecord: Record<string, string> = {};
      try {
        urlSchema.parse(sourceUrl);
      } catch (e) {
        if (e instanceof z.ZodError) {
          errorRecord[sourceUrl] = e.errors
            .map((a) => `👉 ${a.message} ${sourceUrl}`)
            .join("\n");
        }
      }
      setErrors(Object.values(errorRecord));
    }
  }, [sourceUrl]);

  return (
    <form className="space-y-6 text-black " onSubmit={onSubmitHandler}>
      <p className="text-red small whitespace-pre-line">{errors.join("\n")}</p>
      <label>
        <small className="text-slate-500">
          Valid url starts with http:// or https://
        </small>
        <Input
          value={sourceUrl}
          onChange={(e) => {
            setSourceUrl(e.target.value);
          }}
          placeholder="Source URL"
        />
      </label>
      <div>
        <label>
          <small className="text-slate-500">
            Add question context for newsletter data
          </small>
          <Textarea
            value={questionContext}
            onChange={(e) => setQuestionContext(e.target.value)}
            disabled={isLoading}
            placeholder="Newsletter context"
          />
        </label>
      </div>
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading}>
          Generate
        </Button>
      </div>
    </form>
  );
};

export default NewsletterGeneratorForm;

"use client";

import { FormEvent, useContext, useEffect, useState } from "react";

import { z } from "zod";

import { ChatContext } from "@/app/_context/chatContext";
import { getClientAskChat } from "@/app/_models/chat";
import Button from "@/app/_atoms/button/Button";
import Spinner from "@/app/_atoms/spinner/Spinner";
import Textarea from "@/app/_atoms/textarea/Textarea";
import Select, { Option } from "@/app/_molecules/select/Select";
import { QuestionType } from "@/app/types";
import { DocFile, getClientFiles } from "@/app/_models/file";

const contentSchema = z
  .object({
    content: z
      .string()
      .min(2, { message: "👉 min 2 characters" })
      .max(5000, { message: "👉 max 5000 characters" }),
    isRagAndDocument: z.boolean(),
  })
  .refine((data) => !data.isRagAndDocument, {
    message: "👉 for RAG you need to select document",
  });

const options: Option<QuestionType>[] = [
  {
    label: "Chat",
    value: "chat",
  },
  {
    label: "AWS",
    value: "aws",
  },
  {
    label: "RAG",
    value: "rag",
  },
];

const ChatForm = ({ id }: { id: string }) => {
  const [content, setContent] = useState("");
  const [questionType, setQuestionType] = useState<QuestionType>(options[0].value);
  const [documents, setDocuments] = useState<DocFile[]>([]);
  const [document, setDocument] = useState<Option<string>>();
  const [errors, setErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { setQuestions } = useContext(ChatContext);

  const documentOptions = documents.map(({ id, filename }) => ({
    label: filename,
    value: id,
  }));

  const cleanContent = content.trim();
  const isError = errors.length > 0;

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const documentId = document?.value || "";
    if (questionType === "rag" && !documentId) {
      return;
    }

    if (isError) {
      return;
    }
    setIsLoading(true);
    try {
      const res = await getClientAskChat(
        id,
        content,
        questionType,
        documentId
      );
      if (res.ok) {
        const resData = await res.json();
        setQuestions(resData);
        setContent("");
      }
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    try {
      contentSchema.parse({
        content: cleanContent,
        isRagAndDocument: questionType === "rag" && !document?.value,
      });
      setErrors([]);
    } catch (error) {
      if (error instanceof z.ZodError) {
        setErrors(error.errors.map((e) => e.message));
      }
    }
  }, [cleanContent, questionType, document]);

  useEffect(() => {
    getClientFiles()
      .then((res) => {
        return res.json();
      })
      .then((files: DocFile[]) => {
        setDocuments(files);
      });
  }, []);

  return (
    <form className="space-y-5" onSubmit={onSubmitHandler}>
      <Select<QuestionType>
        options={options}
        onOptionChange={(o) => {
          setQuestionType(o.value);
        }}
        defaultOption={options[0]}
        label="Select mode"
      />
      {questionType === "rag" && (
        <Select<string>
          options={documentOptions}
          onOptionChange={(o) => {
            setDocument(o);
          }}
          defaultOption={document}
          label="Select document"
        />
      )}
      <div className="relative">
        {isLoading && <Spinner className="absolute-center" />}
        <label>
          <Textarea
            value={content}
            placeholder="Write your question here..."
            onChange={(e) => setContent(e.target.value)}
            disabled={isLoading}
          />
          <small className="text-red whitespace-pre-line">
            {errors.join("\n")}
          </small>
        </label>
      </div>
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading || isError}>
          Ask {questionType}
        </Button>
      </div>
    </form>
  );
};

export default ChatForm;

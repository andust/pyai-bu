"use client";

import { ChangeEvent, FormEvent, useState } from "react";

import Button from "../../_atoms/button/Button";
import { useRouter } from "next/navigation";

const UploadFilesForm = () => {
  const router = useRouter()
  const [files, setFiles] = useState<File[]>([]);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (files.length === 0) return;

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_GENIA_SERIVCE}/api/v1/file/upload`,
        {
          credentials: "include",
          method: "POST",
          cache: "no-cache",
          body: formData,
        }
      );
      
      if (res.ok) {
        router.push("/files")
      } else {
        console.error("Files upload failed");
      }
    } catch (error) {
      console.error("An error occurred", error);
    }
  };

  const onChangeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };
  return (
    <form className="space-y-5 text-black" onSubmit={onSubmitHandler}>
      <label>
        <small className="text-slate-500">File</small>
        <input type="file" onChange={onChangeHandler} multiple />
      </label>
      <div className="flex justify-end">
        <Button type="submit">Submit</Button>
      </div>
    </form>
  );
};

export default UploadFilesForm;

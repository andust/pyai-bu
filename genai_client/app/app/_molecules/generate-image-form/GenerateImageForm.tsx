"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import Button from "../../_atoms/button/Button";
import Input from "@/app/_atoms/input/Input";
import Select, { Option } from "@/app/_molecules/select/Select";


const options: Option<string>[] = [
  {
    label: "1024x1024",
    value: "1024x1024",
  },
  {
    label: "Horizontal 1792x1024",
    value: "1792x1024",
  },
  {
    label: "Vertical 1024x1792",
    value: "1024x1792",
  },
];

const GenerateImageForm = () => {
  const router = useRouter();

  const [content, setContent] = useState("");
  const [imageSize, setImageSize] = useState<string>(options[0].value);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (content.trim()) {
      fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/file/generate-image/`, {
        credentials: "include",
        method: "POST",
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content, image_size: imageSize }),
      }).then(async (res) => {
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data)) {
            router.push(`/files?id=${data[0]["metadata"]["file_id"]}`);
          }
        }
      });
    }
  };

  return (
    <form className="space-y-5 text-black" onSubmit={onSubmitHandler}>
      <label>
        <small className="text-slate-500">Generate file</small>
        <Input
          name="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Generate image"
        />
      </label>
      <Select<string>
        options={options}
        onOptionChange={(o) => {
          setImageSize(o.value);
        }}
        defaultOption={options[0]}
        label="Select size"
      />
      <div className="flex justify-end">
        <Button type="submit">Generate</Button>
      </div>
    </form>
  );
};

export default GenerateImageForm;

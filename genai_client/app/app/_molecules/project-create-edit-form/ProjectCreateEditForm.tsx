"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import Button from "../../_atoms/button/Button";
import Textarea from "../../_atoms/textarea/Textarea";
import Input from "../../_atoms/input/Input";
import Select, { Option } from "../../_molecules/select/Select";

import { ComplexityLevel } from "../../types";

const options: Option<ComplexityLevel>[] = [
  {
    label: "Low",
    value: ComplexityLevel.LOW,
  },
  {
    label: "Medium",
    value: ComplexityLevel.MEDIUM,
  },
  {
    label: "High",
    value: ComplexityLevel.HIGH,
  },
  {
    label: "Critical",
    value: ComplexityLevel.CRITICAL,
  },
];

const ProjectCreateEditForm = () => {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [complexity, setComplexity] = useState(options[0]);
  const [isLoading, setIsLoading] = useState(false);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/project/`, {
      credentials: "include",
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        description,
        complexity: complexity.value,
      }),
    }).then(async (res) => {
      if (res.ok) {
        router.push("/project");
      }
    }).finally(() => {
      setIsLoading(false);
    });
  };

  return (
    <form className="space-y-6 text-black " onSubmit={onSubmitHandler}>
      <label>
        <small className="text-slate-500">Project title</small>
        <Input
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
          }}
        />
      </label>
      <div>
        <label>
          <small className="text-slate-500">Project description</small>
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isLoading}
          />
        </label>
      </div>
      <Select<ComplexityLevel>
        options={options}
        onOptionChange={(o) => {
          setComplexity(o);
        }}
        defaultOption={options[0]}
        label="Select mode"
      />
      <div className="flex justify-end">
        <Button type="submit" disabled={isLoading}>
          Create
        </Button>
      </div>
    </form>
  );
};

export default ProjectCreateEditForm;

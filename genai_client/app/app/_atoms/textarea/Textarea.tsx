import { ChangeEvent } from "react";

interface Props {
  value: string | number;
  name?: string;
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  disabled?:boolean
}

export default function Textarea({
  value,
  name,
  onChange,
  placeholder = "",
  disabled=false
}: Props) {
  const className = [];
  if (disabled) {
    className.push("bg-slate-900")
  }
  return (
    <textarea
      className={className.join(" ")}
      name={name}
      rows={4}
      placeholder={placeholder}
      onChange={onChange}
      value={value}
      disabled={disabled}
    />
  );
}

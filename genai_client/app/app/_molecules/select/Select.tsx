"use client";

import { ReactNode, useEffect, useRef, useState } from "react";

import "./select.css";
import Button from "@/app/_atoms/button/Button";

export interface Option<V> {
  label: string | ReactNode;
  value: V;
}

interface SelectProps<V> {
  options: Option<V>[];
  label: string;
  onOptionChange: (option: Option<V>) => void;
  defaultOption?: Option<V> | null;
}

const Select = <V,>({
  options,
  label,
  onOptionChange,
  defaultOption = null,
}: SelectProps<V>) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState<Option<V> | null>(
    defaultOption
  );
  const selectRef = useRef<HTMLDivElement>(null);

  const showClassName = isOpen ? " show" : "";

  const toggleSelect = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option: Option<V>) => {
    setSelectedOption(option);
    onOptionChange(option);
    setIsOpen(false);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      selectRef.current &&
      !selectRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="relative text-white" ref={selectRef}>
      <Button
        onClick={toggleSelect}
        className="w-full relative z-20 bg-black p-2 border rounded text-left"
      >
        {selectedOption?.label || label}
      </Button>
      <ul
        className={`absolute z-30 w-full mt-1 bg-black border rounded transition-all duration-200 ease-in-out${showClassName}`}
      >
        {options.map((option) => (
          <li
            key={`${option.value}`}
            onClick={() => handleOptionClick(option)}
            className="p-2 hover:bg-gray-700 cursor-pointer"
          >
            {option.label}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Select;

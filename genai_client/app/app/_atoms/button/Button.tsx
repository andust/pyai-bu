import { ChildrenProp, ClassNameProp } from "../../types";

export interface ThemeProp {
  theme?: "base" | "primary" | "danger";
}

interface Props extends ChildrenProp, ClassNameProp, ThemeProp {
  type?: "button" | "submit" | "reset";
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  disabled?: boolean;
}

const THEME_CLASSNAMES = {
  base: "px-3 py-2 border text-white",
  primary: "px-3 py-2 border bg-green text-white",
  danger: "px-3 py-2 border bg-red text-white",
};

export default function Button({
  children,
  className = "",
  type = "button",
  onClick,
  theme = "base",
  disabled = false,
}: Props) {
  const disabledClassName = disabled ? "text-slate-400 bg-slate-300" : "";
  return (
    <button
      className={`${className} ${THEME_CLASSNAMES[theme]} ${disabledClassName}`}
      type={type}
      onClick={onClick && onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

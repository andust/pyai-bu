"use client";

import { FormEvent, useContext, useState } from "react";

import Input from "../../_atoms/input/Input";
import Button from "../../_atoms/button/Button";
import { UserContext } from "../../_context/userContext";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { setUser } = useContext(UserContext);

  const onSubmitHandler = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const res = await fetch(`/api/login`, {
        cache: "no-cache",
        headers: { "Content-Type": "application/json" },
        method: "post",
        body: JSON.stringify({ email, password }),
      });

      const resData = await res.json();
      if (res.ok) {
        setUser(resData);
        window.location.href = "/";
      }
    } catch {}
  };

  const onChangeHandler = (e: FormEvent<HTMLInputElement>) => {
    const target = e.target as HTMLFormElement;
    const setState = { email: setEmail, password: setPassword }[target.name];
    if (setState) {
      setState(target.value);
    }
  };

  return (
    <form className="space-y-5 text-black" onSubmit={onSubmitHandler}>
      <label>
        <small className="text-slate-500">Email</small>
        <Input
          name="email"
          value={email}
          onChange={onChangeHandler}
          placeholder="Email"
        />
      </label>
      <label>
        <small className="text-slate-500">Password</small>
        <Input
          name="password"
          value={password}
          onChange={onChangeHandler}
          type="password"
          placeholder="password"
        />
      </label>
      <div className="flex justify-end">
        <Button type="submit">Submit</Button>
      </div>
    </form>
  );
};

export default LoginForm;

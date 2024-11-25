import { createReducer, on } from "@ngrx/store";
import { clearUser, setUser } from "./user.actions";

export interface UserState {
  email: string | null;
}

export const initialState: UserState = {
  email: null,
};

export const userReducer = createReducer(
  initialState,
  on(setUser, (state, { user }) => ({
    ...state,
    email: user.email,
  })),
  on(clearUser, (state) => ({
    ...state,
    email: null,
  }))
);

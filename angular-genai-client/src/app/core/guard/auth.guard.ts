import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { Store } from "@ngrx/store";
import { setUser } from "../store/user/user.actions";

export const isAuthenticatedGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const store = inject(Store)

  authService.isAuthenticated().subscribe({
    next: (user) => {
      store.dispatch(setUser({ user }));
      return true;
    },
    error: (e) => {
      return router.navigate(["/auth/login"]);
    },
  });

  return true;
};

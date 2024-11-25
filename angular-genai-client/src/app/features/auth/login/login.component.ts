import { Component } from "@angular/core";
import { AuthService } from "../../../core/services/auth.service";
import { FormControl, FormGroup } from "@angular/forms";
import { Router } from "@angular/router";

@Component({
  selector: "app-login",
  standalone: false,
  templateUrl: "./login.component.html",
  styleUrl: "./login.component.scss",
})
export class LoginComponent {
  loginForm = new FormGroup({
    email: new FormControl(""),
    password: new FormControl(""),
  });
  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    const { email, password } = this.loginForm.value;
    if (email && password) {
      this.authService.baseLogin(email, password).subscribe({
        next: () => {
          return this.router.navigate(["/"]);
        },
        error: (e) => {
          console.log(e);
        },
      });
    }
  }
}

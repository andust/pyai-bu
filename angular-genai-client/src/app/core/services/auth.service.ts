import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { catchError, map, Observable, of, Subscription } from "rxjs";
import { User } from "../models/user.model";
import { environment } from "../../../environments/environment";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private accountUrl = `${environment.genAiApiUrl}user`;
  private loginUrl = `${environment.genAiApiUrl}login`;

  constructor(private http: HttpClient) {}

  isAuthenticated(): Observable<User> {
    return this.http.get<User>(this.accountUrl, { withCredentials: true });
  }

  baseLogin(email: string, password: string): Observable<User> {
    return this.http.post<User>(this.loginUrl, { email, password }, { withCredentials: true });
  }
}

import { Injectable } from "@angular/core";
import { environment } from "../../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Chat } from "../models/chat.model";

@Injectable({
  providedIn: "root",
})
export class ChatService {
  private chatListUrl = `${environment.genAiApiUrl}chat/`;
  constructor(private http: HttpClient) {}

  new(): Observable<Chat> {
    return this.http.post<Chat>(this.chatListUrl, null, {
      withCredentials: true,
    });
  }

  list(): Observable<Chat[]> {
    return this.http.get<Chat[]>(this.chatListUrl, { withCredentials: true });
  }

  details(id: string | null): Observable<Chat> {
    return this.http.get<Chat>(`${this.chatListUrl}${id}`, {
      withCredentials: true,
    });
  }

  delete(id: string): Observable<boolean> {
    return this.http.delete<boolean>(`${this.chatListUrl}${id}`, {
      withCredentials: true,
    });
  }
}

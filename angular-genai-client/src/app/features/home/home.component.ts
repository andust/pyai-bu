import { HttpClient } from "@angular/common/http";
import { Component } from "@angular/core";
import { environment } from "../../../environments/environment";
import { Router } from "@angular/router";
import { Chat } from "../../core/models/chat.model";
import { ChatService } from "../../core/services/chat.service";

@Component({
  selector: "app-home",
  standalone: false,

  templateUrl: "./home.component.html",
  styleUrl: "./home.component.scss",
})
export class HomeComponent {
  chats: Chat[];

  constructor(private chatService: ChatService, private router: Router) {
    this.chats = [];
  }

  ngOnInit(): void {
    this.chatService.list().subscribe({
      next: (chats) => {
        this.chats = chats;
      },
    });
  }

  handleNewChat(): void {
    this.chatService.new().subscribe({
      next: ({ id }) => {
        console.log(id);
        return this.router.navigate([`chat/${id}`]);
      },
      error: (err) => {
        console.log(err);
      },
    });
  }
}

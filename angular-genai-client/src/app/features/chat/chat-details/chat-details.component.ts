import { Component } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { switchMap } from "rxjs";
import { ChatService } from "../../../core/services/chat.service";
import { Chat } from "../../../core/models/chat.model";
import { FormControl, FormGroup } from "@angular/forms";
import { Option } from "../../../shared/ui/molecules/select/select.component";

@Component({
  selector: "app-chat-details",
  standalone: false,

  templateUrl: "./chat-details.component.html",
  styleUrl: "./chat-details.component.scss",
})
export class ChatDetailsComponent {
  chat: Chat | null = null;
  chatOptions = [
    { label: "Chat", value: "chat" },
    { label: "RAG", value: "rag" },
  ]

  defaultOption = this.chatOptions[0]

  questionForm = new FormGroup({
    question: new FormControl(""),
    chatMode: new FormControl(""),
  })

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private chatService: ChatService
  ) {}

  ngOnInit(): void {
    this.route.paramMap
      .pipe(switchMap((params) => this.chatService.details(params.get("id"))))
      .subscribe({
        next: (chat) => {
          this.chat = chat;
        },
      });
  }

  handleDeleteConfirmation(chat: Chat | null): void {
    if (chat?.id) {
      this.chatService.delete(chat.id).subscribe({
        next: () => {
          this.router.navigate(["/"]);
        },
      });
    }
  }

  onOptionChange(option: Option<string>) {
    console.log(option)
    this.questionForm.patchValue({
      chatMode: option.value,
    })
  }

  onSubmit(): void {
    console.log(this.questionForm.value);
  }
}

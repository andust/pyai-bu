import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ChatRoutingModule } from './chat-routing.module';
import { ChatDetailsComponent } from './chat-details/chat-details.component';
import { UiModule } from '../../shared/ui/ui.module';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ChatDetailsComponent,
  ],
  imports: [
    CommonModule,
    ChatRoutingModule,
    ReactiveFormsModule,
    UiModule,
  ]
})
export class ChatModule { }

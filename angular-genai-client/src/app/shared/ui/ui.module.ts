import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MainComponent } from './templates/main/main.component';
import { AuthComponent } from './templates/auth/auth.component';
import { ButtonComponent } from './atoms/button/button.component';
import { ConfirmComponent } from './atoms/confirm/confirm.component';
import { SelectComponent } from './molecules/select/select.component';



@NgModule({
  declarations: [
    MainComponent,
    AuthComponent,
    ButtonComponent,
    ConfirmComponent,
    SelectComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [
    ButtonComponent,
    ConfirmComponent,
    SelectComponent
  ]
})
export class UiModule { }

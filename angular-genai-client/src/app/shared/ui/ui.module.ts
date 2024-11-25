import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MainComponent } from './templates/main/main.component';
import { AuthComponent } from './templates/auth/auth.component';



@NgModule({
  declarations: [
    MainComponent,
    AuthComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  // exports: [
  //   MainComponent,
  //   AuthComponent
  // ]
})
export class UiModule { }

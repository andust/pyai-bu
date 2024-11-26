import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { UiModule } from "./shared/ui/ui.module";
import { provideHttpClient } from "@angular/common/http";
import { StoreModule } from "@ngrx/store";
import { userReducer } from "./core/store/user/user.reducer";


@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    StoreModule.forRoot({
      user: userReducer,
    }),
    UiModule,
  ],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent],
})
export class AppModule {}

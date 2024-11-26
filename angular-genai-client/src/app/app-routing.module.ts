import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { MainComponent } from "./shared/ui/templates/main/main.component";
import { AuthComponent } from "./shared/ui/templates/auth/auth.component";
import { isAuthenticatedGuard } from "./core/guard/auth.guard";

const routes: Routes = [
  {
    path: "",
    component: MainComponent,
    canActivate: [isAuthenticatedGuard],
    children: [
      {
        path: "",
        loadChildren: () =>
          import("./features/home/home.module").then((m) => m.HomeModule),
      },
      {
        path: "chat",
        loadChildren: () =>
          import("./features/chat/chat.module").then((m) => m.ChatModule),
      },
      {
        path: "files",
        loadChildren: () =>
          import("./features/files/files.module").then((m) => m.FilesModule),
      },
    ],
  },
  {
    path: "auth",
    component: AuthComponent,
    children: [
      {
        path: "",
        loadChildren: () =>
          import("./features/auth/auth.module").then((m) => m.AuthModule),
      },
    ],
  },
  { path: 'chat', loadChildren: () => import('./features/chat/chat.module').then(m => m.ChatModule) },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

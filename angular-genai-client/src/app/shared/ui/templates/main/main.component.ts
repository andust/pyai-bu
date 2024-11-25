import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../../../../core/models/user.model';
import { select, Store } from '@ngrx/store';
import { selectUser } from '../../../../core/store/user/user.selectors';
import { UserState } from '../../../../core/store/user/user.reducer';
import { AppState } from '../../../../core/store/app.state';

@Component({
  selector: 'app-main',
  standalone: false,
  
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
 userEmail: string | null

 constructor(private stroe: Store<AppState>) {
  this.userEmail = null;
  this.stroe.pipe(select(selectUser)).subscribe({
    next: (value) => {
      this.userEmail = value.email
    }
  })
 }
}

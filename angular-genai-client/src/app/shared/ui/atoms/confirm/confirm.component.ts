import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-confirm',
  standalone: false,
  
  templateUrl: './confirm.component.html',
  styleUrl: './confirm.component.scss'
})
export class ConfirmComponent {
  @Output() onConfirm = new EventEmitter<void>();

  isVisible = true;

  handleClick() {
    this.isVisible = false;
  }

  handleConfirm() {
    this.onConfirm.emit();
    this.isVisible = true;
  }

  handleCancel() {
    this.isVisible = true;
  }
}

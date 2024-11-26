import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-button',
  standalone: false,
  
  templateUrl: './button.component.html',
  styleUrl: './button.component.scss'
})
export class ButtonComponent {
  @Input() theme: "base" | "primary" | "danger" = "base";
  @Input() type: "button" | "submit" | "reset" = "button";
  @Input() disabled: boolean = false;
  @Input() className: string = "";
  @Output() onClick = new EventEmitter<Event>();

  get cssClasses(): string {
    const themeClassNames: Record<string, string> = {
      base: 'px-3 py-2 border text-white',
      primary: 'px-3 py-2 border bg-green text-white',
      danger: 'px-3 py-2 border bg-red text-white',
    }

    const disabledClassName = this.disabled ? " text-slate-400 bg-slate-300" : "";
    return `${this.className} ${themeClassNames[this.theme]}${disabledClassName}`
  }

  handleClick(event: Event) {
    if (!this.disabled) {
      this.onClick.emit(event);
    }
  }
}

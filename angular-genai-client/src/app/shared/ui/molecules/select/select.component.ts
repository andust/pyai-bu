import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnDestroy,
  OnInit,
  Output,
  ViewChild,
} from "@angular/core";

export interface Option<V> {
  label: string | HTMLElement;
  value: V;
}

@Component({
  selector: "app-select",
  standalone: false,

  templateUrl: "./select.component.html",
  styleUrl: "./select.component.scss",
})
export class SelectComponent<V> implements OnInit, OnDestroy {
  @Input() options: Option<V>[] = [];
  @Input() label: string = "Select an option";
  @Input() defaultOption: Option<V> | null = null;
  @Output() optionChange = new EventEmitter<Option<V>>();

  @ViewChild("selectRef") selectRef!: ElementRef;

  isOpen = false;
  selectedOption: Option<V> | null = null;

  private handleClickOutside = (event: MouseEvent): void => {
    if (
      this.selectRef &&
      !this.selectRef.nativeElement.contains(event.target)
    ) {
      this.isOpen = false;
    }
  };

  ngOnInit(): void {
    if (this.defaultOption) {
      this.selectedOption = this.defaultOption;
      this.optionChange.emit(this.defaultOption);
    }
    document.addEventListener("mousedown", this.handleClickOutside);
  }

  ngOnDestroy(): void {
    document.removeEventListener("mousedown", this.handleClickOutside);
  }

  toggleSelect() {
    this.isOpen = !this.isOpen;
  }

  handleOptionClick(option: Option<V>) {
    this.selectedOption = option;
    this.optionChange.emit(option);
    this.isOpen = false;
  }
}

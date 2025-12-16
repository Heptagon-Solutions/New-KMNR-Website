import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'paginator',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './paginator.component.html',
  styleUrls: ['./paginator.component.scss'],
})
export class PaginatorComponent {
  @Input() public totalPages: number | undefined = undefined;
  @Input() public currentPage: number = 0;

  @Output() public changePage = new EventEmitter<number>();

  protected goToPage(newPage: number) {
    if (newPage >= 0) {
      this.changePage.emit(newPage);
    }
  }
}

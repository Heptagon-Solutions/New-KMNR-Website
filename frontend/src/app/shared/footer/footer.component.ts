import { Component, HostListener, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterPositionService } from 'src/app/services/footer-position.service';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent implements OnInit {
  private footerContainerElement: HTMLElement | null = null;

  constructor(private readonly footerPositionService: FooterPositionService) {}

  ngOnInit(): void {
    this.footerContainerElement = document.getElementById('footer');
  }

  @HostListener('window:resize', ['$event'])
  @HostListener('window:scroll', ['$event'])
  emitFooterRelativePosition(event: Event): void {
    if (this.footerContainerElement) {
      const yPosition = this.footerContainerElement.getBoundingClientRect().top;
      const viewportRelativeYPosition = window.innerHeight - yPosition;

      const lastFooterPosition =
        this.footerPositionService.topOfFooterPosition.getValue();
      if (viewportRelativeYPosition >= 0) {
        this.footerPositionService.topOfFooterPosition.next(
          viewportRelativeYPosition
        );
      } else if (viewportRelativeYPosition <= 0 && lastFooterPosition > 0) {
        this.footerPositionService.topOfFooterPosition.next(0);
      }
    }
  }
}

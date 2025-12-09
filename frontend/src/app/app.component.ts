import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  OnDestroy,
  ViewChild,
} from '@angular/core';

import { FooterPositionService } from './services/footer-position.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements AfterViewInit, OnDestroy {
  @ViewChild('mainContent')
  public mainContent!: ElementRef;
  @ViewChild('footer')
  public footer: ElementRef | undefined;

  private readonly changes: MutationObserver;

  constructor(private readonly footerPositionService: FooterPositionService) {
    this.changes = new MutationObserver(_ => {
      this.emitFooterRelativePosition();
    });
  }

  public ngAfterViewInit(): void {
    // Refresh the footer's tracked position every time the DOM changes, so that the webstream popup is always correctly placed
    this.changes.observe(this.mainContent.nativeElement, {
      attributes: true,
      childList: true,
      characterData: true,
      subtree: true,
    });
  }

  public ngOnDestroy(): void {
    this.changes.disconnect();
  }

  @HostListener('window:resize')
  @HostListener('window:scroll')
  public emitFooterRelativePosition(): void {
    if (this.footer) {
      const footerElement = this.footer.nativeElement;
      const yPosition = footerElement.getBoundingClientRect().top;
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

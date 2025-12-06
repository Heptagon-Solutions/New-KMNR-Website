import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavigationEnd, Router } from '@angular/router';
import { filter, Subscription } from 'rxjs';

import { FooterPositionService } from 'src/app/services/footer-position.service';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent implements OnInit, OnDestroy {
  private footerContainerElement: HTMLElement | null = null;

  private routerSubscription: Subscription | null = null;

  constructor(
    private readonly footerPositionService: FooterPositionService,
    private readonly router: Router
  ) {}

  public ngOnInit(): void {
    this.footerContainerElement = document.getElementById('footer');

    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(_ => this.emitFooterRelativePosition());
  }

  public ngOnDestroy(): void {
    this.routerSubscription?.unsubscribe();
  }

  @HostListener('window:resize')
  @HostListener('window:scroll')
  public emitFooterRelativePosition(): void {
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

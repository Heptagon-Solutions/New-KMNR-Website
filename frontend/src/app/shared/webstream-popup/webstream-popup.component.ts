import { Component, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { filter, Subscription } from 'rxjs';

import { Show } from 'src/models/show';
import { FooterPositionService } from 'src/app/services/footer-position.service';
import { ShowService } from 'src/app/services/show.service';
import { WebstreamPlayerComponent } from 'src/app/shared/webstream-player/webstream-player.component';

@Component({
  selector: 'webstream-popup',
  standalone: true,
  imports: [CommonModule, WebstreamPlayerComponent],
  templateUrl: './webstream-popup.component.html',
  styleUrls: ['./webstream-popup.component.scss'],
})
export class WebstreamPopupComponent implements OnDestroy {
  protected currentShow: Show | null = null;

  protected popupPosition: number = 0;

  private readonly currentShowSubscription: Subscription;
  private readonly footerPositionSubscription: Subscription;

  constructor(
    private readonly showService: ShowService,
    private readonly footerPositionService: FooterPositionService
  ) {
    this.currentShowSubscription = this.showService
      .getCurrentShow()
      .subscribe((show: Show | null) => (this.currentShow = show));

    // Move the popup above the footer when it is visible
    this.footerPositionSubscription =
      this.footerPositionService.topOfFooterPosition
        .pipe(filter(y => y >= 0))
        .subscribe(y => {
          this.popupPosition = y;
        });
  }

  public ngOnDestroy() {
    this.currentShowSubscription.unsubscribe();
    this.footerPositionSubscription.unsubscribe();
  }
}

import { Component, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';

import { Show } from 'src/models/show';
import { ShowService } from 'src/app/services/show.service';
import { ProfileImageComponent } from '../profile-image/profile-image.component';

@Component({
  selector: 'on-air',
  standalone: true,
  imports: [CommonModule, ProfileImageComponent],
  templateUrl: './on-air.component.html',
  styleUrls: ['./on-air.component.scss'],
})
export class OnAirComponent implements OnDestroy {
  protected currentShow: Show | null = null;

  private readonly currentShowSubscription: Subscription;

  constructor(private readonly showService: ShowService) {
    this.currentShowSubscription = this.showService
      .getCurrentShow()
      .subscribe((show: Show | null) => (this.currentShow = show));
  }

  public ngOnDestroy(): void {
    this.currentShowSubscription.unsubscribe();
  }
}

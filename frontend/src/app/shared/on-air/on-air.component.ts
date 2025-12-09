import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';

import { Show } from 'src/models/show';
import { ShowService } from 'src/app/services/show.service';

@Component({
  selector: 'on-air',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './on-air.component.html',
  styleUrls: ['./on-air.component.scss'],
})
export class OnAirComponent {
  protected currentShow: Show | null = null;

  private readonly currentShowSubscription: Subscription;

  constructor(private readonly showService: ShowService) {
    this.currentShowSubscription = this.showService
      .getCurrentShow()
      .subscribe((show: Show | null) => (this.currentShow = show));
  }

  public ngOnDestory() {
    this.currentShowSubscription.unsubscribe();
  }
}

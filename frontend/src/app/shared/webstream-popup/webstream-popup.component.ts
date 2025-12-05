import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs';

import { Show } from 'src/models/show';
import { DayOfTheWeek } from 'src/models/general';
import { WebstreamPlayerComponent } from '../webstream-player/webstream-player.component';
import { FooterPositionService } from 'src/app/services/footer-position.service';

const SAMPLE_SHOW: Show = {
  id: 1,
  name: 'Morning Vibes',
  shortDesc: 'short desc',
  day: DayOfTheWeek.Monday,
  startTime: 8,
  endTime: 10,
  semester: {
    term: 'Fall',
    year: 2026,
  },
  hosts: [
    {
      id: 1,
      djName: 'DJ John',
      userName: 'dj-john-username',
    },
    {
      id: 2,
      djName: 'DJ Sarah',
      userName: 'dj-sarah-username',
    },
  ],
};

@Component({
  selector: 'webstream-popup',
  standalone: true,
  imports: [CommonModule, WebstreamPlayerComponent],
  templateUrl: './webstream-popup.component.html',
  styleUrls: ['./webstream-popup.component.scss'],
})
export class WebstreamPopupComponent {
  protected currentShow: Show | undefined = undefined;

  protected popupPosition: number = 0;

  constructor(private readonly footerPositionService: FooterPositionService) {
    // Dummy data for now
    this.currentShow = SAMPLE_SHOW;

    // Move the popup above the footer when it is visible
    this.footerPositionService.topOfFooterPosition
      .pipe(filter(y => y >= 0))
      .subscribe(y => {
        this.popupPosition = y;
      });
  }
}

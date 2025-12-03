import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Show } from 'src/models/show';
import { DayOfTheWeek } from 'src/models/general';

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
  selector: 'webstream-player',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './webstream-player.component.html',
  styleUrls: ['./webstream-player.component.scss'],
})
export class WebstreamPlayerComponent {
  protected currentShow: Show | undefined = undefined;

  constructor() {
    // Dummy data for now
    this.currentShow = SAMPLE_SHOW;
  }
}

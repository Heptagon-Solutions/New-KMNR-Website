import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DayOfTheWeek } from 'src/models/general';
import { Show } from 'src/models/show';

const SAMPLE_DATA = [
  {
    id: 1,
    name: 'Morning Vibes',
    shortDesc: 'short description',
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
    ],
  },
  {
    id: 2,
    name: 'Rock Hour',
    shortDesc: 'short desc',
    day: DayOfTheWeek.Tuesday,
    startTime: 15,
    endTime: 16,
    semester: {
      term: 'Fall',
      year: 2026,
    },
    hosts: [
      {
        id: 2,
        djName: 'DJ Sarah',
        userName: 'dj-sarah-user-name',
      },
      {
        id: 3,
        djName: 'DJ Other',
        userName: 'dj-other-user-name',
      },
    ],
  },
];

@Component({
  selector: 'show-schedule',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './show-schedule.component.html',
  styleUrls: ['./show-schedule.component.scss'],
})
export class ShowScheduleComponent implements OnInit {
  public readonly times = Array(24)
    .fill(0)
    .map((x, i) => i);

  public readonly days: DayOfTheWeek[] = [
    DayOfTheWeek.Sunday,
    DayOfTheWeek.Monday,
    DayOfTheWeek.Tuesday,
    DayOfTheWeek.Wednesday,
    DayOfTheWeek.Thursday,
    DayOfTheWeek.Friday,
    DayOfTheWeek.Saturday,
  ];

  public shows: Show[] = [];

  ngOnInit(): void {
    this.loadShows();

    console.log('Days are:', this.days);
  }

  loadShows(): void {
    // TODO: Replace with actual ShowService call
    // this.showService.getShows().subscribe(shows => this.shows = shows);

    // Mock data for now
    this.shows = SAMPLE_DATA;
  }

  public parseTime(t: number): string {
    if (t == 0) return 'Midnight';
    else if (t > 0 && t < 12) return t + ':00 AM';
    else if (t == 12) return 'Noon';
    else if (t > 12 && t <= 23) {
      return t - 12 + ':00 PM';
    }
    return 'Error';
  }

  public getShowForTimeSlot(time: number, day: DayOfTheWeek): Show | null {
    return (
      this.shows.find(
        show =>
          show.day === day && time >= show.startTime && time < show.endTime
      ) || null
    );
  }
}

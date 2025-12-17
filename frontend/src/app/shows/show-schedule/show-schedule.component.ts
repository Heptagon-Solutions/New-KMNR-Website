import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DayOfTheWeek } from 'src/models/general';
import { Show } from 'src/models/show';
import { DEMO_SCHEDULE } from 'src/app/services/demo_schedule';

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
    this.shows = DEMO_SCHEDULE;
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

  public getShowForStartingTime(time: number, day: DayOfTheWeek): Show | null {
    return (
      this.shows.find(show => show.day === day && time == show.startTime) ||
      null
    );
  }

  public getShowDuration(time: number, day: DayOfTheWeek): number {
    let show: Show | null = this.getShowForTimeSlot(time, day);
    return show === null ? 0 : Math.abs(show.endTime - show.startTime);
  }
}

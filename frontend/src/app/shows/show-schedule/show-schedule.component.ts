import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScheduleService } from 'src/app/services/schedule.service';
import { ShowScheduleEntry } from 'src/models';

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
    
  public timeslots: { [time: number]: ShowScheduleEntry[] } = {};
  public readonly days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  constructor(private scheduleService: ScheduleService) {}

  async ngOnInit() {
    await this.loadSchedule();
  }

  private async loadSchedule() {
    try {
      this.timeslots = this.scheduleService.getTimeslots();
    } catch (error) {
      console.error('Error loading schedule:', error);
    }
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

  public getShow(time: number, dayOfWeek: number): ShowScheduleEntry | null {
    const shows = this.timeslots[time] || [];
    return shows.find(show => show.day_of_week === dayOfWeek && 
                     time >= show.start_time && 
                     time < show.end_time) || null;
  }

  public getShowSpan(show: ShowScheduleEntry): number {
    return show.end_time - show.start_time;
  }
}

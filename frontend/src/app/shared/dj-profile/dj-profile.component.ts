import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { DJ, ShowScheduleEntry } from 'src/models';

import { OnAirComponent } from '../on-air/on-air.component';
import { DJService } from '../dj.service';
import { ScheduleService } from '../../services/schedule.service';


@Component({
  selector: 'dj-profile',
  standalone: true,
  imports: [CommonModule, OnAirComponent],
  templateUrl: './dj-profile.component.html',
  styleUrls: ['./dj-profile.component.scss'],
})
export class DJProfileComponent implements OnInit {
  public dj: DJ | undefined = undefined;
  public djShows: ShowScheduleEntry[] = [];

  constructor(
    private readonly route: ActivatedRoute,
    private readonly djService: DJService,
    private readonly scheduleService: ScheduleService
  ) {}

  async ngOnInit() {
    const djId = Number(this.route.snapshot.paramMap.get('id')) || 1;
    
    try {
      this.dj = await this.djService.getDJ(djId);
      this.djShows = await this.scheduleService.getShowsForDJ(djId);
    } catch (error) {
      console.error('Error loading DJ profile:', error);
    }
  }

  getDayName(dayOfWeek: number): string {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[dayOfWeek] || '';
  }

  formatTime(hour: number): string {
    if (hour === 0) return '12:00 AM';
    else if (hour < 12) return `${hour}:00 AM`;
    else if (hour === 12) return '12:00 PM';
    else return `${hour - 12}:00 PM`;
  }
}

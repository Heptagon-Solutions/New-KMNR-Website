import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Show {
  id: string;
  name: string;
  dj: string;
  day: string;
  start_time: number;
  end_time: number;
}

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

  public readonly days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  
  public shows: Show[] = [];

  ngOnInit(): void {
    this.loadShows();
  }

  loadShows(): void {
    // TODO: Replace with actual ShowService call
    // this.showService.getShows().subscribe(shows => this.shows = shows);
    
    // Mock data for now
    this.shows = [
      {
        id: '1',
        name: 'Morning Vibes',
        dj: 'DJ John',
        day: 'Monday',
        start_time: 8,
        end_time: 10
      },
      {
        id: '2',
        name: 'Rock Hour',
        dj: 'DJ Sarah',
        day: 'Tuesday',
        start_time: 15,
        end_time: 16
      }
    ];
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

  public getShowForTimeSlot(time: number, day: string): Show | null {
    return this.shows.find(show => 
      show.day === day && 
      time >= show.start_time && 
      time < show.end_time
    ) || null;
  }
}

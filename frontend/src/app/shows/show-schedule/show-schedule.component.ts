import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'show-schedule',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './show-schedule.component.html',
  styleUrls: ['./show-schedule.component.scss'],
})
export class ShowScheduleComponent {
  public readonly times = Array(24)
    .fill(0)
    .map((x, i) => i);

  public parseTime(t: number): string {
    console.log(t);
    if (t == 0) return 'Midnight';
    else if (t > 0 && t < 12) return t + ':00 AM';
    else if (t == 12) return 'Noon';
    else if (t > 12 && t <= 23) {
      return t - 12 + ':00 PM';
    }
    return 'Error';
  }
}

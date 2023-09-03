import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OnAirComponent } from '../shared/on-air/on-air.component';
import { Semester } from 'src/models';
import { ShowService } from './show.service';
import { ShowScheduleComponent } from './show-schedule/show-schedule.component';

@Component({
  selector: 'shows',
  standalone: true,
  imports: [CommonModule, OnAirComponent, ShowScheduleComponent],
  templateUrl: './shows.component.html',
  styleUrls: ['./shows.component.scss'],
})
export class ShowsComponent {
  public semester: Semester | undefined = undefined;

  constructor(private readonly showService: ShowService) {
    showService.getSemester().then((s: Semester) => (this.semester = s));
  }
}

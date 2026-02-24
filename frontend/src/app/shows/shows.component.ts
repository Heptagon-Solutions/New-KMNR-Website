import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Semester } from 'src/models/general';
import { ShowService } from 'src/app/services/show.service';
import { ShowScheduleComponent } from './show-schedule/show-schedule.component';

@Component({
  selector: 'shows',
  standalone: true,
  imports: [CommonModule, ShowScheduleComponent],
  templateUrl: './shows.component.html',
  styleUrls: ['./shows.component.scss'],
})
export class ShowsComponent {
  protected semester: Semester | undefined = undefined;

  constructor(private readonly showService: ShowService) {
    this.showService
      .getSemester()
      .subscribe((s: Semester) => (this.semester = s));
  }
}

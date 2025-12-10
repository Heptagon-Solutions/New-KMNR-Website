import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { DayOfTheWeek, Semester } from 'src/models/general';
import { Show } from 'src/models/show';

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
      profileImg: null,
    },
    {
      id: 2,
      djName: 'DJ Sarah',
      userName: 'dj-sarah-username',
      profileImg: null,
    },
  ],
};

@Injectable({
  providedIn: 'root',
})
export class ShowService {
  public getSemester(): Observable<Semester> {
    return of({
      term: 'Summer',
      year: 1999,
    });
  }

  /** Returns an observable that emits the current show, and emits the next one when the time slot changes over. */
  public getCurrentShow(): Observable<Show | null> {
    return of(SAMPLE_SHOW);
  }
}

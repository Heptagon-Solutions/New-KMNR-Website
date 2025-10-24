import { Injectable } from '@angular/core';

import { Semester } from 'src/models/general';

@Injectable({
  providedIn: 'root',
})
export class ShowService {
  constructor() {}

  public async getSemester(): Promise<Semester> {
    return {
      term: 'Summer',
      year: 1999,
    };
  }
}

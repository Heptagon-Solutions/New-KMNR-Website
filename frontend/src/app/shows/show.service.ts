import { Injectable } from '@angular/core';
import { Semester } from 'src/models';

const URL = 'http://localhost:3000/';

@Injectable({
  providedIn: 'root',
})
export class ShowService {
  constructor() {}

  public async getSemester(): Promise<Semester> {
    const response = await fetch(URL + 'misc');
    const data = await response.json();

    return {
      term: this.parseTerm(data.term),
      year: data.year,
    };
  }

  private parseTerm(term: string): string {
    return term === 'SP' ? 'Spring ' : 'Fall ';
  }
}

import { Injectable } from '@angular/core';
import { TownAndCampusNewsEntry } from 'src/models';

const URL = 'http://localhost:3000/townAndCampusNews/';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor() {}

  async getNewsEntries(): Promise<TownAndCampusNewsEntry[]> {
    const data = await fetch(URL);
    return await data.json();
  }
}

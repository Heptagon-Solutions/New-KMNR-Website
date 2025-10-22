import { Injectable } from '@angular/core';

import { API_URL } from 'src/constants';
import { TownAndCampusNewsEntryDetailed } from 'src/models/town-and-campus-news';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor() {}

  public async getNewsEntries(): Promise<TownAndCampusNewsEntryDetailed[]> {
    const data = await fetch(API_URL + 'admin/news');
    return await data.json();
  }
}

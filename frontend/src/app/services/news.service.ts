import { Injectable } from '@angular/core';

import { API_URL } from 'src/constants';
import {
  TownAndCampusNewsEntry,
  TownAndCampusNewsEntryDetailed,
} from 'src/models/models';

const URL = 'http://localhost:3000/townAndCampusNews/';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor() {}

  public async getNewsEntries(): Promise<TownAndCampusNewsEntry[]> {
    const data = await fetch(URL);
    return await data.json();
  }

  public async getAllNewsEntries(): Promise<TownAndCampusNewsEntryDetailed[]> {
    const data = await fetch(API_URL + 'admin/news');
    return await data.json();
  }
}

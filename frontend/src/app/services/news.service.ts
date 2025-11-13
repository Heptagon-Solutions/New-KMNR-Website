import { Injectable } from '@angular/core';

import { API_URL } from 'src/constants';
import {
  TownAndCampusNewsEntry,
  TownAndCampusNewsEntryDetailed,
} from 'src/models';

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

  public async createNewsEntry(newsEntry: TownAndCampusNewsEntryDetailed): Promise<TownAndCampusNewsEntryDetailed> {
    const response = await fetch(API_URL + 'admin/news', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newsEntry),
    });
    return await response.json();
  }

  public async updateNewsEntry(id: string, newsEntry: Partial<TownAndCampusNewsEntryDetailed>): Promise<TownAndCampusNewsEntryDetailed> {
    const response = await fetch(API_URL + `admin/news/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newsEntry),
    });
    return await response.json();
  }

  public async deleteNewsEntry(id: string): Promise<void> {
    await fetch(API_URL + `admin/news/${id}`, {
      method: 'DELETE',
    });
  }
}

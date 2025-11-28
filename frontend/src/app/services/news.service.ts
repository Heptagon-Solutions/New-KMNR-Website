import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_URL } from 'src/constants';
import { TownAndCampusNewsEntryDetailed } from 'src/models/town-and-campus-news';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor(private readonly http: HttpClient) {}

  public getNewsEntries(): Observable<TownAndCampusNewsEntryDetailed[]> {
    return this.http.get<TownAndCampusNewsEntryDetailed[]>(
      API_URL + 'admin/news'
    );
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

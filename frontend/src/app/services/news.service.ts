import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

import { API_URL } from 'src/constants';
import {
  TownAndCampusNewsEntryDetailed,
  TownAndCampusNewsEntryFormData,
} from 'src/models/town-and-campus-news';

const NEWS_API_URL = API_URL + 'admin/news';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor(private readonly http: HttpClient) {}

  public getNewsCount(): Observable<number> {
    return this.http
      .get<{ count: number }>(API_URL + 'count/news')
      .pipe(map(resp => resp.count));
  }

  public getNewsEntries(
    count: number,
    page: number
  ): Observable<TownAndCampusNewsEntryDetailed[]> {
    return this.http
      .get<{ townAndCampusNews: TownAndCampusNewsEntryDetailed[] }>(
        NEWS_API_URL,
        { params: { count, page } }
      )
      .pipe(map(resp => resp.townAndCampusNews));
  }

  public createNewsEntry(
    newsEntryData: TownAndCampusNewsEntryFormData
  ): Observable<TownAndCampusNewsEntryDetailed> {
    console.debug('Creating new Town & Campus News entry:', newsEntryData);

    return this.http.post<TownAndCampusNewsEntryDetailed>(
      API_URL + 'news',
      newsEntryData
    );
  }

  public async updateNewsEntry(
    id: string,
    newsEntry: Partial<TownAndCampusNewsEntryDetailed>
  ): Promise<TownAndCampusNewsEntryDetailed> {
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

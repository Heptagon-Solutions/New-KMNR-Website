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
}

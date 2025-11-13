import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable, of } from 'rxjs';

import { API_URL } from 'src/constants';
import { DJ, DJProfile } from 'src/models/dj';

const DJS_API_URL = API_URL + 'api/djs';

@Injectable({
  providedIn: 'root',
})
export class DJService {
  constructor(private readonly http: HttpClient) {}

  public getDJCount(): Observable<number> {
    return this.http
      .get<{ count: number }>(API_URL + 'api/count/djs')
      .pipe(map(resp => resp.count));
  }

  /**
   * Fetch paginated list of users.
   * @param count Number of users to return
   * @param page Pagination offset. Page 1 contains users 1 to `count`, page 2 contains `count + 1` to `2 * count`.
   */
  public getDJs(count: number, page: number): Observable<DJ[]> {
    return this.http
      .get<{ djs: DJ[] }>(DJS_API_URL, { params: { count, page } })
      .pipe(map(resp => resp.djs));
  }

  public getDJProfile(id: number): Observable<DJProfile> {
    return this.http.get<DJProfile>(DJS_API_URL + '/' + id);
  }
}

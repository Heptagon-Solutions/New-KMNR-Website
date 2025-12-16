import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

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

  public createDJ(
    userId: number,
    djName: string,
    trainingSemesterId: number,
    trainerId: number | null = null
  ): Observable<DJProfile> {
    const data = { userId, djName, trainingSemesterId, trainerId };
    return this.http.post<DJProfile>(DJS_API_URL, data);
  }

  /** Returns the new profileImg value for DJ of given id. */
  public updateDJProfileImg(id: number, newImage: File): Observable<string> {
    const formData = new FormData();
    formData.append('image', newImage);
    return this.http
      .post<{ id: number; profileImg: string }>(
        `${DJS_API_URL}/${id}/profile-image`,
        formData
      )
      .pipe(map(resp => resp.profileImg));
  }

  /**
   * Edit a DJ's name or profile description (or both).
   * If a parameter is null, it will NOT be updated.
   */
  public updateDJInfo(
    id: number,
    newName: string | null = null,
    newDesc: string | null = null
  ): Observable<void> {
    const formData = new FormData();

    if (newName) {
      // Do not allow empty DJ names
      formData.append('djName', newName);
    }
    if (newDesc !== null) {
      // Allow empty descriptions, but null means do not edit
      formData.append('profileDesc', newDesc);
    }

    return this.http.patch(`${DJS_API_URL}/${id}`, formData).pipe(
      map(_ => {
        return;
      })
    );
  }
}

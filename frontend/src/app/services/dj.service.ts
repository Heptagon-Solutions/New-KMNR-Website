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

  public getAllDJs(): Observable<DJ[]> {
    return this.http
      .get<{ djs: DJ[] }>(DJS_API_URL)
      .pipe(map(resp => resp.djs));
  }

  public getDJProfile(id: number): Observable<DJProfile> {
    return of({
      id: id,
      djName: 'Fake DJ 1',
      desc: 'noise',
    });
  }
}

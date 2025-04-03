import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_URL } from 'src/constants';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private readonly http: HttpClient) {}

  public login$(email: string, pass: string): Observable<{ message: string }> {
    const body = { email, pass };
    return this.http.post<{ message: string }>(API_URL + 'login', body, {
      withCredentials: true,
    });
  }

  public signup$(
    name: string,
    email: string,
    pass: string
  ): Observable<{ message: string }> {
    const body = { name, email, pass };
    return this.http.post<{ message: string }>(API_URL + 'signup', body);
  }
}

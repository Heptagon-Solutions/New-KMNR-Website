import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_URL } from 'src/constants';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private readonly http: HttpClient) {}

  public authenticate$(): Observable<{ message: string }> {
    return this.http.get<{ message: string }>(API_URL + 'authenticate', {
      // withCredentials must be added for cookies to be sent or set
      withCredentials: true,
    });
  }

  public login$(email: string, pass: string): Observable<{ message: string }> {
    const body = { email, pass };
    return this.http.post<{ message: string }>(API_URL + 'login', body, {
      // withCredentials must be added for cookies to be sent or set
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

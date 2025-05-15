import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { API_URL } from 'src/constants';

interface SuccessfulLoginResponse {
  success: boolean;
  userId: number;
  role: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private userId: number | null = null;
  private role: string = 'dj';

  constructor(private readonly http: HttpClient) {}

  public authenticate$(): Observable<{ message: string }> {
    return this.http.get<{ message: string }>(API_URL + 'authenticate', {
      // withCredentials must be added for cookies to be sent or set
      withCredentials: true,
    });
  }

  public login$(
    email: string,
    pass: string
  ): Observable<SuccessfulLoginResponse> {
    const body = { email, pass };
    return this.http
      .post<SuccessfulLoginResponse>(API_URL + 'login', body, {
        // withCredentials must be added for cookies to be sent or set
        withCredentials: true,
      })
      .pipe(tap(data => this.setState(data)));
  }

  public signup$(
    name: string,
    email: string,
    pass: string
  ): Observable<SuccessfulLoginResponse> {
    const body = { name, email, pass };
    return this.http
      .post<SuccessfulLoginResponse>(API_URL + 'signup', body, {
        // withCredentials must be added for cookies to be sent or set
        withCredentials: true,
      })
      .pipe(tap(data => this.setState(data)));
  }

  public isLoggedIn(): boolean {
    return this.userId !== null;
  }

  public getUserId(): number | null {
    return this.userId;
  }

  public getRole(): string | null {
    if (this.userId) {
      return this.role;
    } else {
      return null;
    }
  }

  private setState(loginResponse: SuccessfulLoginResponse) {
    if (loginResponse.success) {
      this.userId = loginResponse.userId;
      this.role = loginResponse.role;
    } else {
      this.clearState();
    }
  }

  private clearState() {
    this.userId = null;
  }
}

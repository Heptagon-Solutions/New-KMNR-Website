import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

import { API_URL } from 'src/constants';
import { User } from 'src/models/user';

const USERS_API_URL = API_URL + 'api/users';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private readonly http: HttpClient) {}

  public getUserCount(): Observable<number> {
    return this.http
      .get<{ count: number }>(API_URL + 'api/count/users')
      .pipe(map(resp => resp.count));
  }

  /**
   * Fetch paginated list of users.
   * @param count Number of users to return
   * @param page Pagination offset. Page 1 contains users 1 to `count`, page 2 contains `count + 1` to `2 * count`.
   */
  public getUsers(count: number, page: number): Observable<User[]> {
    return this.http
      .get<{ users: User[] }>(USERS_API_URL, { params: { count, page } })
      .pipe(map(response => response.users));
  }

  public getUser(userId: number): Observable<User> {
    return this.http.get<User>(USERS_API_URL + '/' + userId);
  }

  public createUser(
    email: string,
    name: string,
    password: string,
    role: string | null = null
  ): Observable<User> {
    const data = { email, name, password, role };
    return this.http.post<User>(USERS_API_URL, data);
  }
}

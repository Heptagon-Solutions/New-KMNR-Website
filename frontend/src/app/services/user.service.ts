import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { User } from 'src/models/user';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor() {}

  private readonly userDummyData: User[] = [
    {
      id: 1,
      name: 'Fake User',
      email: 'fake@e.mail',
      role: 'user',
    },
    {
      id: 2,
      name: 'Fake DJ',
      email: 'fake2@e.mail',
      role: 'dj',
    },
    {
      id: 3,
      name: 'Fake Admin',
      email: 'fake3@e.mail',
      role: 'admin',
    },
  ];

  /**
   * Fetch paginated list of users.
   * @param count Number of users to return
   * @param page Offset. Page 1 contains users 1 to `count`, page 2 contains `count + 1` to `2 * count`.
   */
  public getUsers(count: number, page: number): Observable<User[]> {
    const start = count * page;
    const end = start + count;
    return of(this.userDummyData.slice(start, end));
  }

  public getUserCount(): Observable<number> {
    return of(this.userDummyData.length);
  }

  public getUser(id: number): Observable<User> {
    return of(this.userDummyData[id]);
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { User } from 'src/models/user';

import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'admin-users',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss'],
})
export class AdminUsersComponent {
  protected userList: User[] = [];
  protected page: number = 0;

  /** Returns undefined if we're still waiting on an API response. */
  protected get totalPages(): number | undefined {
    if (this.totalUsers) {
      return Math.ceil(this.totalUsers / this.usersPerPage);
    } else {
      return undefined;
    }
  }

  private readonly usersPerPage: number = 25;

  private totalUsers: number | undefined = undefined;

  constructor(private readonly userService: UserService) {
    userService
      .getUserCount()
      .subscribe(userCount => (this.totalUsers = userCount));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0) {
      this.page = newPage;

      this.userService
        .getUsers(this.usersPerPage, this.page)
        .subscribe((users: User[]) => (this.userList = users));
    }
  }
}

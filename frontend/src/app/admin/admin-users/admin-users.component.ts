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

  protected get totalPages(): number {
    return Math.ceil(this.totalUsers / this.listSize);
  }

  private readonly listSize: number = 25;

  private totalUsers: number = 0;

  constructor(private readonly userService: UserService) {
    userService
      .getUserCount()
      .subscribe(userCount => (this.totalUsers = userCount));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0 && newPage < this.totalPages) {
      this.page = newPage;

      this.userService
        .getUsers(this.listSize, this.page)
        .subscribe((users: User[]) => (this.userList = users));
    }
  }
}

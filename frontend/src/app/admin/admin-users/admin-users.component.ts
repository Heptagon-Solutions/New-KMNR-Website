import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

import { User } from 'src/models/user';

import { UserService } from 'src/app/services/user.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'admin-users',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss'],
})
export class AdminUsersComponent {
  protected userList: User[] = [];
  protected page: number = 0;

  protected newUserName = new FormControl('');
  protected newUserEmail = new FormControl('');
  protected newUserRole = new FormControl('User');
  protected newUserPassword = new FormControl('');

  protected newUserErrorMessage: string | null = null;

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

  public createUser() {
    if (!this.newUserName.value) {
      this.newUserErrorMessage = "User's name is required";
      return;
    } else if (!this.newUserEmail.value) {
      this.newUserErrorMessage = "User's email is required";
      return;
    } else if (!this.newUserPassword.value) {
      this.newUserErrorMessage = "User's password is required";
      return;
    }

    this.userService
      .createUser(
        this.newUserEmail.value,
        this.newUserName.value,
        this.newUserPassword.value,
        this.newUserRole.value
      )
      .subscribe({
        next: () => {
          this.newUserErrorMessage = null;
          // Reload current page, it case it appears there
          this.goToPage(this.page);
        },
        error: (err: HttpErrorResponse) =>
          (this.newUserErrorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
      });
  }
}

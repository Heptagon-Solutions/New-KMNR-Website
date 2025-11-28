import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormControl,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

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
  protected readonly newUserForm = new FormGroup({
    name: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    role: new FormControl('User', { nonNullable: true }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  protected newUserErrorMessage: string | null = null;

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

  public createUser(event: SubmitEvent) {
    // Don't reload the page
    event.preventDefault();

    if (this.newUserForm.valid) {
      const newUser = this.newUserForm.getRawValue();

      this.userService
        .createUser(newUser.email, newUser.name, newUser.password, newUser.role)
        .subscribe({
          next: (user: User) => {
            this.newUserErrorMessage = `User "${user.name}" added with ID: ${user.id}!`;
            // Reload user list, in case it appears there
            this.goToPage(this.page);
          },
          error: (err: HttpErrorResponse) =>
            (this.newUserErrorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
        });
    } else {
      // Trigger validator error CSS styling
      this.newUserForm.markAllAsTouched();
      this.newUserErrorMessage =
        'Errors in form. Ensure all required fields are filled.';
    }
  }
}

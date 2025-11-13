import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService, User } from '../../services/user.service';

@Component({
  selector: 'admin-users',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss']
})
export class AdminUsersComponent implements OnInit {
  users: User[] = [];
  newUser: Partial<User> = {
    username: '',
    email: '',
    role: 'dj'
  };

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.userService.getUsers().subscribe(
      (users: User[]) => {
        this.users = users;
      },
      (error) => {
        console.error('Error loading users:', error);
      }
    );
  }

  addUser(): void {
    if (this.newUser.username && this.newUser.email && this.newUser.role) {
      this.userService.createUser(this.newUser).subscribe(
        (user: User) => {
          this.users.push(user);
          this.newUser = { username: '', email: '', role: 'dj' };
        },
        (error) => {
          console.error('Error creating user:', error);
        }
      );
    }
  }

  editUser(user: User): void {
    // TODO: Implement edit functionality
    console.log('Edit user:', user);
  }

  deleteUser(userId: string): void {
    if (confirm('Are you sure you want to delete this user?')) {
      this.userService.deleteUser(userId).subscribe(
        () => {
          this.users = this.users.filter(user => user.id !== userId);
        },
        (error) => {
          console.error('Error deleting user:', error);
        }
      );
    }
  }
}

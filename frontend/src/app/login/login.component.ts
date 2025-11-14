import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface User {
  username: string;
  role: 'admin' | 'dj' | 'user';
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class LoginComponent implements OnInit {
  username = '';
  password = '';
  loggedInUser: User | null = null;
  loginError = '';

  constructor(private router: Router) {}

  ngOnInit() {}

  onLogin() {
    // Mock authentication - replace with real authentication service
    if (this.username === 'admin' && this.password === 'admin123') {
      this.loggedInUser = { username: this.username, role: 'admin' };
      this.loginError = '';
    } else if (this.username === 'dj' && this.password === 'dj123') {
      this.loggedInUser = { username: this.username, role: 'dj' };
      this.loginError = '';
    } else if (this.username && this.password) {
      this.loggedInUser = { username: this.username, role: 'user' };
      this.loginError = '';
    } else {
      this.loginError = 'Please enter username and password';
    }
  }

  onLogout() {
    this.loggedInUser = null;
    this.username = '';
    this.password = '';
    this.loginError = '';
  }

  navigateToAdmin() {
    this.router.navigate(['/admin']);
  }

  isAdmin(): boolean {
    return this.loggedInUser?.role === 'admin';
  }
}

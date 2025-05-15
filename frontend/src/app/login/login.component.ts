import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [CommonModule, RouterModule],
  standalone: true,
})
export class LoginComponent implements OnInit {
  protected backendMsg: string | null = null;

  constructor(private readonly auth: AuthenticationService) {}

  ngOnInit() {}

  public authenticate() {
    this.auth.authenticate$().subscribe({
      next: m => (this.backendMsg = m.message),
      error: e => {
        console.error('Error while authenticating:', e);
        this.backendMsg = e.message;
      },
    });
  }

  public login(email: string, password: string, rememberMe: boolean = false) {
    // TODO: Validation
    this.auth.login$(email, password).subscribe({
      next: m => {
        return;
      },
      error: e => {
        console.error('Error while logging in:', e);
        this.backendMsg = e.message;
      },
    });
  }

  public signup(
    name: string,
    email: string,
    password: string,
    rememberMe: boolean = false
  ) {
    // TODO: Validation
    this.auth.signup$(name, email, password).subscribe({
      next: m => {
        return;
      },
      error: e => {
        console.error('Error while signing up:', e);
        this.backendMsg = e.message;
      },
    });
  }

  public getAuthState(): string {
    const userId = this.auth.getUserId();
    const role = this.auth.getRole();

    return (userId || 'Not logged in') + '; ' + (role || 'no role');
  }
}

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

  public login(email: string, password: string) {
    this.auth.login$(email, password).subscribe({
      next: m => (this.backendMsg = m.message),
      error: e => (this.backendMsg = e.message),
    });
  }
}

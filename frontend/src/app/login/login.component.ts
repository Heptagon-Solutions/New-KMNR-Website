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

  public login() {
    this.auth
      .login$('testuser@temp.com', 'testpass')
      .subscribe(m => (this.backendMsg = m.message));
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { BannerComponent } from '../shared/banner/banner.component';

interface BackendData {
  msg: string;
}

@Component({
  selector: 'home',
  standalone: true,
  imports: [CommonModule, BannerComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  public backendMsg: string = 'Waiting for backend to respond...';

  constructor(private readonly http: HttpClient) {
    // Using an Observable to change component data
    this.getBackendMsg$().subscribe({
      next: (data: BackendData) => {
        this.backendMsg = data.msg;
      },
      error: (err: string) => {
        this.backendMsg = err;
      },
    });
  }

  // Example of requesting data from the backend, and getting it back as an Observable
  private getBackendMsg$(): Observable<BackendData> {
    return this.http
      .get<BackendData>('http://localhost:5000/data')
      .pipe(catchError(this.errorHandler$));
  }

  // Handles all errors from Observable before use in frontend
  private errorHandler$(error: HttpErrorResponse): Observable<BackendData> {
    if (error.error === 0) {
      throw 'An client-side or network error occured.';
    } else {
      if (error.status === 0) {
        throw 'Error when contacting the backend. Do you have it running?';
      } else {
        throw `Error: backend returned code ${error.status}.`;
      }
    }
  }
}

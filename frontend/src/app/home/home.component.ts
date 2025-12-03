import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_URL } from 'src/constants';
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
    // Example of processing an Observable to edit component data
    this.getBackendMsg$().subscribe({
      // This is called if everything goes well
      next: (data: BackendData) => {
        this.backendMsg = data.msg;
      },
      // This is called when errorHandler$ `throw`s an error
      error: (err: string) => {
        this.backendMsg = 'ERROR: ' + err;
      },
    });
  }

  /**
   * Example of requesting data from the backend and getting it back as an Observable.
   */
  private getBackendMsg$(): Observable<BackendData> {
    return this.http.get<BackendData>(API_URL + 'data').pipe(
      // errorHandler$ is called if the request throws an error (HttpErrorResponse)
      catchError(this.errorHandler$)
    );
  }

  /**
   * Observable error handlers can either:
   * 1. Process the error and return an Observable, which makes everything continue like nothing happened, or,
   * 2. Throw an error, triggering the 'error' function in the subscription.
   * @throws a string error message describing what went wrong.
   */
  private errorHandler$(error: HttpErrorResponse): Observable<BackendData> {
    if (error.error === 0) {
      throw 'An client-side or network error occured.';
    } else {
      if (error.status === 0) {
        throw 'Problem contacting backend. Do you have it running?';
      } else {
        throw `backend returned code ${error.status}.`;
      }
    }
  }

  /**
   * Opens the KMNR featured playlist in Spotify web player
   */
  openSpotifyPlaylist(): void {
    // Example playlist URL - replace with actual KMNR playlist
    const playlistUrl = 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M';
    window.open(playlistUrl, '_blank');
  }
}

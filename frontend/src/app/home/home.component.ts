import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_URL } from 'src/constants';
import { BannerComponent } from '../shared/banner/banner.component';
import { BlogService } from '../services/blog.service';
import { PlaylistService } from '../services/playlist.service';
import { BlogPost, PlaylistEntry, Playlist } from 'src/models';

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
export class HomeComponent implements OnInit {
  public backendMsg: string = 'Waiting for backend to respond...';
  public latestBlogPost: BlogPost | null = null;
  public latestPlayedSong: PlaylistEntry | null = null;
  public latestPlaylist: Playlist | null = null;

  constructor(
    private readonly http: HttpClient,
    private readonly router: Router,
    private readonly blogService: BlogService,
    private readonly playlistService: PlaylistService
  ) {
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

  async ngOnInit() {
    await this.loadHomeData();
  }

  private async loadHomeData() {
    try {
      const [blogPosts, recentTracks, allPlaylists] = await Promise.all([
        this.blogService.getAllPosts(),
        this.playlistService.getRecentTracks(1),
        this.playlistService.getAllPlaylists()
      ]);

      this.latestBlogPost = blogPosts.length > 0 ? blogPosts[0] : null;
      this.latestPlayedSong = recentTracks.length > 0 ? recentTracks[0] : null;
      this.latestPlaylist = allPlaylists.length > 0 ? allPlaylists[0] : null;
    } catch (error) {
      console.error('Error loading home data:', error);
    }
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

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  formatPlayTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  }

  truncateContent(content: string, maxLength: number = 200): string {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  }

  navigateToBlogPost(id: number) {
    this.router.navigate(['/blog', id]);
  }

  navigateToPlaylist(id: number) {
    this.router.navigate(['/playlist', id]);
  }
}

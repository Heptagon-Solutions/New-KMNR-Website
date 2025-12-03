import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { SpotifyService } from '../services/spotify.service';

@Component({
  selector: 'app-spotify-callback',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spotify-callback.component.html',
  styleUrls: ['./spotify-callback.component.scss']
})
export class SpotifyCallbackComponent implements OnInit {
  isProcessing = true;
  message = 'Processing Spotify authorization...';
  
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private spotifyService: SpotifyService
  ) {}

  async ngOnInit(): Promise<void> {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const error = urlParams.get('error');
      
      if (error) {
        console.error('Spotify auth error:', error);
        this.message = 'Authorization failed. Redirecting...';
        setTimeout(() => this.router.navigate(['/spotify']), 2000);
        return;
      }
      
      if (code) {
        this.message = 'Exchanging authorization code for access token...';
        const success = await this.spotifyService.handleCallback();
        
        if (success) {
          this.message = 'Authorization successful! Redirecting...';
          const returnPath = this.spotifyService.getReturnPath();
          setTimeout(() => this.router.navigate([returnPath]), 1000);
        } else {
          this.message = 'Authorization failed. Redirecting...';
          setTimeout(() => this.router.navigate(['/spotify']), 2000);
        }
      } else {
        this.message = 'No authorization code found. Redirecting...';
        setTimeout(() => this.router.navigate(['/spotify']), 2000);
      }
    } catch (error) {
      console.error('Callback processing failed:', error);
      this.message = 'Authorization processing failed. Redirecting...';
      setTimeout(() => this.router.navigate(['/spotify']), 2000);
    } finally {
      this.isProcessing = false;
    }
  }
}

import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SpotifyService } from '../../services/spotify.service';
import { PlaylistService } from '../../services/playlist.service';
import { SpotifyPlaylist } from '../../../models/playlist';

@Component({
  selector: 'app-admin-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.scss'],
})
export class AdminHomeComponent implements OnInit {
  isSpotifyConnected = false;
  playlists: SpotifyPlaylist[] = [];
  isLoading = false;

  constructor(
    private spotifyService: SpotifyService,
    private playlistService: PlaylistService
  ) {}

  ngOnInit() {
    this.spotifyService.isAuthenticated$.subscribe(isAuth => {
      this.isSpotifyConnected = isAuth;
    });
    this.loadPlaylists();
  }

  connectToSpotify() {
    this.spotifyService.authorize();
  }

  loadPlaylists() {
    this.isLoading = true;
    this.playlistService.getPlaylists().subscribe({
      next: (playlists) => {
        this.playlists = playlists;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load playlists:', error);
        this.isLoading = false;
      }
    });
  }

  publishToSpotify(playlist: SpotifyPlaylist) {
    if (!this.isSpotifyConnected) {
      alert('Please connect to Spotify first');
      return;
    }

    this.playlistService.publishToSpotify(playlist.id).subscribe({
      next: (response) => {
        playlist.spotify_playlist_id = response.spotify_playlist_id;
        alert(`Playlist published to Spotify! ${response.tracks_added} tracks added.`);
        
        if (response.spotify_url) {
          window.open(response.spotify_url, '_blank');
        }
      },
      error: (error) => {
        console.error('Failed to publish playlist:', error);
        alert('Failed to publish playlist to Spotify');
      }
    });
  }

  openSpotifyPlaylist(spotifyPlaylistId: string) {
    window.open(`https://open.spotify.com/playlist/${spotifyPlaylistId}`, '_blank');
  }
}

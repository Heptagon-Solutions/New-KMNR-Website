import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { PlaylistProfile } from 'src/models/playlist';
import { SpotifyService } from 'src/app/services/spotify.service';
import { PlaylistService } from 'src/app/services/playlist.service';

@Component({
  selector: 'dj-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dj-home.component.html',
  styleUrls: ['./dj-home.component.scss'],
})
export class DJHomeComponent implements OnInit {
  isSpotifyConnected = false;
  playlists: PlaylistProfile[] = [];
  isLoading = false;

  constructor(
    private readonly spotifyService: SpotifyService,
    private readonly playlistService: PlaylistService
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
      next: playlists => {
        this.playlists = playlists;
        this.isLoading = false;
      },
      error: error => {
        console.error('Failed to load playlists:', error);
        this.isLoading = false;
      },
    });
  }

  publishToSpotify(playlist: PlaylistProfile) {
    if (!this.isSpotifyConnected) {
      alert('Please connect to Spotify first');
      return;
    }

    this.playlistService.publishToSpotify(playlist.id).subscribe({
      next: response => {
        playlist.spotifyPlaylistId = response.spotify_playlist_id;
        alert(
          `Playlist published to Spotify! ${response.tracks_added} tracks added.`
        );

        if (response.spotify_url) {
          window.open(response.spotify_url, '_blank');
        }
      },
      error: error => {
        console.error('Failed to publish playlist:', error);
        alert('Failed to publish playlist to Spotify');
      },
    });
  }

  openSpotifyPlaylist(spotifyPlaylistId: string) {
    if (spotifyPlaylistId) {
      window.open(
        `https://open.spotify.com/playlist/${spotifyPlaylistId}`,
        '_blank'
      );
    }
  }
}

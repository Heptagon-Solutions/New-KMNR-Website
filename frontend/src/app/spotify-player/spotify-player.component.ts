import { Component, OnInit } from '@angular/core';
import { SpotifyService, SpotifyTrack, SpotifyPlaylist, SpotifyUserProfile } from '../services/spotify.service';

@Component({
  selector: 'app-spotify-player',
  templateUrl: './spotify-player.component.html',
  styleUrls: ['./spotify-player.component.scss']
})
export class SpotifyPlayerComponent implements OnInit {
  isConnected = false;
  hasSpotifyPremium = false;
  userProfile: SpotifyUserProfile | null = null;
  searchResults: SpotifyTrack[] = [];
  userPlaylists: SpotifyPlaylist[] = [];
  currentTrack: SpotifyTrack | null = null;
  errorMessage = '';

  constructor(private spotifyService: SpotifyService) {}

  ngOnInit() {
    // Check if already authenticated
    this.spotifyService.isAuthenticated$.subscribe(isAuth => {
      this.isConnected = isAuth;
      if (isAuth) {
        this.loadUserProfile();
      }
    });
  }

  async connectSpotify() {
    try {
      this.errorMessage = '';
      await this.spotifyService.authorize();
    } catch (error) {
      this.errorMessage = 'Failed to connect to Spotify: ' + error;
    }
  }

  async disconnect() {
    try {
      this.spotifyService.clearTokens();
      this.isConnected = false;
      this.userProfile = null;
      this.searchResults = [];
      this.userPlaylists = [];
      this.currentTrack = null;
      this.errorMessage = '';
    } catch (error) {
      this.errorMessage = 'Error during disconnect: ' + error;
    }
  }

  async loadUserProfile() {
    try {
      this.userProfile = await this.spotifyService.getUserProfile();
      // Check if user has Premium (required for playback control)
      this.hasSpotifyPremium = this.userProfile.product === 'premium';
    } catch (error) {
      console.error('Failed to load user profile:', error);
    }
  }

  async search(query: string) {
    if (!query.trim()) return;

    try {
      this.errorMessage = '';
      const results = await this.spotifyService.searchTracks(query, 10);
      this.searchResults = results;
    } catch (error) {
      this.errorMessage = 'Search failed: ' + error;
      this.searchResults = [];
    }
  }

  async playTrack(track: SpotifyTrack) {
    if (!this.hasSpotifyPremium) {
      this.errorMessage = 'Spotify Premium required for playback control';
      return;
    }

    try {
      this.errorMessage = '';
      await this.spotifyService.playTrack(track.uri);
      this.currentTrack = track;
    } catch (error) {
      this.errorMessage = 'Playback failed: ' + error;
    }
  }

  async playPlaylist(playlist: SpotifyPlaylist) {
    if (!this.hasSpotifyPremium) {
      this.errorMessage = 'Spotify Premium required for playback control';
      return;
    }

    try {
      this.errorMessage = '';
      await this.spotifyService.playPlaylist(playlist.id);
    } catch (error) {
      this.errorMessage = 'Playlist playback failed: ' + error;
    }
  }

  async getUserPlaylists() {
    try {
      this.errorMessage = '';
      this.userPlaylists = await this.spotifyService.getUserPlaylists();
    } catch (error) {
      this.errorMessage = 'Failed to load playlists: ' + error;
    }
  }

  async pausePlayback() {
    if (!this.hasSpotifyPremium) return;

    try {
      await this.spotifyService.pausePlayback();
    } catch (error) {
      this.errorMessage = 'Failed to pause: ' + error;
    }
  }

  async resumePlayback() {
    if (!this.hasSpotifyPremium) return;

    try {
      await this.spotifyService.resumePlayback();
    } catch (error) {
      this.errorMessage = 'Failed to resume: ' + error;
    }
  }

  async nextTrack() {
    if (!this.hasSpotifyPremium) return;

    try {
      await this.spotifyService.nextTrack();
      // Optionally refresh current track info
    } catch (error) {
      this.errorMessage = 'Failed to skip: ' + error;
    }
  }

  async previousTrack() {
    if (!this.hasSpotifyPremium) return;

    try {
      await this.spotifyService.previousTrack();
      // Optionally refresh current track info
    } catch (error) {
      this.errorMessage = 'Failed to go back: ' + error;
    }
  }
}
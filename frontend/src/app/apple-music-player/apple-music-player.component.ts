import { Component, OnInit } from '@angular/core';
import { AppleMusicService } from '../services/apple-music.service';

@Component({
  selector: 'apple-music-player',
  templateUrl: './apple-music-player.component.html',
  styleUrls: ['./apple-music-player.component.scss']
})
export class AppleMusicPlayerComponent implements OnInit {
  searchResults: any[] = [];
  userPlaylists: any[] = [];
  recentlyPlayed: any[] = [];
  errorMessage: string = '';

  constructor(public appleMusicService: AppleMusicService) {}

  ngOnInit(): void {
    // Component initialization is handled by the service
  }

  async login(): Promise<void> {
    try {
      const success = await this.appleMusicService.login();
      if (!success) {
        this.errorMessage = 'Failed to login to Apple Music';
      } else {
        this.errorMessage = '';
      }
    } catch (error) {
      this.errorMessage = 'Login error: ' + error;
    }
  }

  async logout(): Promise<void> {
    try {
      await this.appleMusicService.logout();
      this.userPlaylists = [];
      this.recentlyPlayed = [];
      this.errorMessage = '';
    } catch (error) {
      this.errorMessage = 'Logout error: ' + error;
    }
  }

  async search(term: string): Promise<void> {
    if (!term.trim()) return;

    try {
      this.errorMessage = '';
      const results = await this.appleMusicService.search(term, ['songs'], 10);
      this.searchResults = results.songs?.data || [];
    } catch (error) {
      this.errorMessage = 'Search error: ' + error;
      this.searchResults = [];
    }
  }

  async playSong(songId: string): Promise<void> {
    try {
      this.errorMessage = '';
      await this.appleMusicService.playSong(songId);
    } catch (error) {
      this.errorMessage = 'Playback error: ' + error;
    }
  }

  async playPlaylist(playlistId: string): Promise<void> {
    try {
      this.errorMessage = '';
      await this.appleMusicService.playPlaylist(playlistId);
    } catch (error) {
      this.errorMessage = 'Playlist playback error: ' + error;
    }
  }

  async pause(): Promise<void> {
    try {
      await this.appleMusicService.pause();
    } catch (error) {
      this.errorMessage = 'Pause error: ' + error;
    }
  }

  async stop(): Promise<void> {
    try {
      await this.appleMusicService.stop();
    } catch (error) {
      this.errorMessage = 'Stop error: ' + error;
    }
  }

  async skipToNext(): Promise<void> {
    try {
      await this.appleMusicService.skipToNextItem();
    } catch (error) {
      this.errorMessage = 'Skip error: ' + error;
    }
  }

  async skipToPrevious(): Promise<void> {
    try {
      await this.appleMusicService.skipToPreviousItem();
    } catch (error) {
      this.errorMessage = 'Skip error: ' + error;
    }
  }

  async getUserPlaylists(): Promise<void> {
    try {
      this.errorMessage = '';
      this.userPlaylists = await this.appleMusicService.getUserPlaylists();
    } catch (error) {
      this.errorMessage = 'Error loading playlists: ' + error;
    }
  }

  async getRecentlyPlayed(): Promise<void> {
    try {
      this.errorMessage = '';
      this.recentlyPlayed = await this.appleMusicService.getUserRecentlyPlayed();
    } catch (error) {
      this.errorMessage = 'Error loading recently played: ' + error;
    }
  }
}

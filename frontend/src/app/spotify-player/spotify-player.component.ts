import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Subscription, interval } from 'rxjs';
import { SpotifyService } from '../services/spotify.service';

interface PlaybackState {
  device?: {
    id: string;
    name: string;
    type: string;
    volume_percent: number;
    is_active: boolean;
  };
  repeat_state: string;
  shuffle_state: boolean;
  context?: {
    type: string;
    href: string;
    external_urls: { spotify: string };
    uri: string;
  };
  timestamp: number;
  progress_ms: number;
  is_playing: boolean;
  item?: {
    album: {
      name: string;
      images: Array<{ url: string; height: number; width: number }>;
    };
    artists: Array<{ name: string }>;
    duration_ms: number;
    external_urls: { spotify: string };
    id: string;
    name: string;
    uri: string;
  };
}

interface Device {
  id: string;
  name: string;
  type: string;
  is_active: boolean;
  volume_percent: number;
}

@Component({
  selector: 'app-spotify-player',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spotify-player.component.html',
  styleUrls: ['./spotify-player.component.css']
})
export class SpotifyPlayerComponent implements OnInit, OnDestroy {
  playbackState: PlaybackState | null = null;
  devices: Device[] = [];
  isAuthenticated = false;
  isLoading = false;
  error: string | null = null;

  private pollingSubscription?: Subscription;
  private readonly baseUrl = 'http://127.0.0.1:5001';

  constructor(
    private http: HttpClient,
    private spotifyService: SpotifyService
  ) {}

  ngOnInit() {
    this.spotifyService.isAuthenticated$.subscribe(auth => {
      this.isAuthenticated = auth;
      if (auth) {
        this.loadPlaybackState();
        this.loadDevices();
        this.startPolling();
      } else {
        this.stopPolling();
      }
    });
  }

  ngOnDestroy() {
    this.stopPolling();
  }

  private startPolling() {
    this.pollingSubscription = interval(3000).subscribe(() => {
      this.loadPlaybackState();
    });
  }

  private stopPolling() {
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
    }
  }

  async loadPlaybackState() {
    try {
      const response = await this.makeRequest('/me/player');
      if (response.ok) {
        const data = await response.json();
        this.playbackState = data;
        this.error = null;
      } else if (response.status === 204) {
        this.playbackState = null;
      }
    } catch (error) {
      console.error('Error loading playback state:', error);
      this.error = 'Failed to load playback state';
    }
  }

  async loadDevices() {
    try {
      const response = await this.makeRequest('/me/player/devices');
      if (response.ok) {
        const data = await response.json();
        this.devices = data.devices || [];
      }
    } catch (error) {
      console.error('Error loading devices:', error);
    }
  }

  async play() {
    try {
      this.isLoading = true;
      await this.makeRequest('/me/player/play', { method: 'PUT' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error playing:', error);
      this.error = 'Failed to play';
    } finally {
      this.isLoading = false;
    }
  }

  async pause() {
    try {
      this.isLoading = true;
      await this.makeRequest('/me/player/pause', { method: 'PUT' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error pausing:', error);
      this.error = 'Failed to pause';
    } finally {
      this.isLoading = false;
    }
  }

  async skipNext() {
    try {
      this.isLoading = true;
      await this.makeRequest('/me/player/next', { method: 'POST' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error skipping to next:', error);
      this.error = 'Failed to skip';
    } finally {
      this.isLoading = false;
    }
  }

  async skipPrevious() {
    try {
      this.isLoading = true;
      await this.makeRequest('/me/player/previous', { method: 'POST' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error skipping to previous:', error);
      this.error = 'Failed to skip';
    } finally {
      this.isLoading = false;
    }
  }

  async toggleShuffle() {
    try {
      this.isLoading = true;
      const newState = !this.playbackState?.shuffle_state;
      await this.makeRequest(`/me/player/shuffle?state=${newState}`, { method: 'PUT' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error toggling shuffle:', error);
      this.error = 'Failed to toggle shuffle';
    } finally {
      this.isLoading = false;
    }
  }

  async toggleRepeat() {
    try {
      this.isLoading = true;
      const currentState = this.playbackState?.repeat_state || 'off';
      const nextState = currentState === 'off' ? 'context' : 
                       currentState === 'context' ? 'track' : 'off';
      await this.makeRequest(`/me/player/repeat?state=${nextState}`, { method: 'PUT' });
      setTimeout(() => this.loadPlaybackState(), 500);
    } catch (error) {
      console.error('Error toggling repeat:', error);
      this.error = 'Failed to toggle repeat';
    } finally {
      this.isLoading = false;
    }
  }

  async setVolume(volume: number) {
    try {
      await this.makeRequest(`/me/player/volume?volume_percent=${volume}`, { method: 'PUT' });
    } catch (error) {
      console.error('Error setting volume:', error);
      this.error = 'Failed to set volume';
    }
  }

  async transferPlayback(deviceId: string) {
    try {
      this.isLoading = true;
      await this.makeRequest('/me/player', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          device_ids: [deviceId],
          play: true
        })
      });
      setTimeout(() => {
        this.loadPlaybackState();
        this.loadDevices();
      }, 1000);
    } catch (error) {
      console.error('Error transferring playback:', error);
      this.error = 'Failed to transfer playback';
    } finally {
      this.isLoading = false;
    }
  }

  async seekToPosition(positionMs: number) {
    try {
      await this.makeRequest(`/me/player/seek?position_ms=${positionMs}`, { method: 'PUT' });
    } catch (error) {
      console.error('Error seeking:', error);
      this.error = 'Failed to seek';
    }
  }

  private async makeRequest(endpoint: string, options: RequestInit = {}) {
    return fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
  }

  async authenticate() {
    await this.spotifyService.authorize();
  }

  formatTime(ms: number): string {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

  getProgressPercent(): number {
    if (!this.playbackState?.item?.duration_ms || !this.playbackState?.progress_ms) {
      return 0;
    }
    return (this.playbackState.progress_ms / this.playbackState.item.duration_ms) * 100;
  }

  onProgressClick(event: MouseEvent) {
    if (!this.playbackState?.item?.duration_ms) return;

    const progressBar = event.currentTarget as HTMLElement;
    const rect = progressBar.getBoundingClientRect();
    const percent = (event.clientX - rect.left) / rect.width;
    const positionMs = Math.floor(percent * this.playbackState.item.duration_ms);
    
    this.seekToPosition(positionMs);
  }

  onVolumeChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const volume = parseInt(target.value);
    this.setVolume(volume);
  }

  getDeviceIcon(deviceType: string): string {
    switch (deviceType?.toLowerCase()) {
      case 'computer': return 'desktop';
      case 'smartphone': return 'mobile-alt';
      case 'speaker': return 'volume-up';
      case 'tv': return 'tv';
      case 'automobile': return 'car';
      case 'game_console': return 'gamepad';
      case 'tablet': return 'tablet-alt';
      default: return 'music';
    }
  }

  getArtistNames(artists?: Array<{ name: string }>): string {
    return artists?.map(a => a.name).join(', ') || '';
  }

  isShuffleActive(): boolean {
    return this.playbackState?.shuffle_state || false;
  }

  isPlaying(): boolean {
    return this.playbackState?.is_playing || false;
  }

  isRepeatActive(): boolean {
    return this.playbackState?.repeat_state !== 'off';
  }

  isRepeatContext(): boolean {
    return this.playbackState?.repeat_state === 'context';
  }

  isRepeatTrack(): boolean {
    return this.playbackState?.repeat_state === 'track';
  }

  getDeviceIconClass(): string {
    return 'fas fa-' + this.getDeviceIcon(this.playbackState?.device?.type || 'unknown');
  }

  getDeviceName(): string {
    return this.playbackState?.device?.name || 'Unknown device';
  }

  getVolumePercent(): number {
    return this.playbackState?.device?.volume_percent || 50;
  }

  togglePlayPause() {
    if (this.isPlaying()) {
      this.pause();
    } else {
      this.play();
    }
  }
}
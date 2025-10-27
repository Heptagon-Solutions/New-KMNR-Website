import { Component, OnInit } from '@angular/core';
import { SpotifyService, SpotifyTrack, SpotifyPlaylist, SpotifyUserProfile, SpotifyPlaylistsResponse } from '../services/spotify.service';

@Component({
  selector: 'app-spotify-playlist',
  templateUrl: './spotify-playlist.component.html',
  styleUrls: ['./spotify-playlist.component.scss']
})
export class SpotifyPlaylistComponent implements OnInit {
  isAuthenticated = false;
  userProfile: SpotifyUserProfile | null = null;
  userPlaylists: SpotifyPlaylist[] = [];
  searchQuery = '';
  searchResults: SpotifyTrack[] = [];
  selectedTracks: SpotifyTrack[] = [];
  currentPlaylist: SpotifyPlaylist | null = null;
  playlistName = 'KMNR Playlist';
  isLoading = false;
  searchPerformed = false;
  currentView: 'playlists' | 'search' | 'tracks' = 'playlists';
  selectedPlaylistForView: SpotifyPlaylist | null = null;

  constructor(private spotifyService: SpotifyService) {}

  async ngOnInit(): Promise<void> {
    this.spotifyService.isAuthenticated$.subscribe(
      authenticated => {
        this.isAuthenticated = authenticated;
        if (authenticated) {
          this.loadUserProfile();
          this.loadUserPlaylists();
        }
      }
    );

    // Handle callback if we're returning from Spotify
    await this.spotifyService.handleCallback();
  }

  async loadUserProfile(): Promise<void> {
    try {
      this.userProfile = await this.spotifyService.getUserProfile();
      console.log('User profile loaded:', this.userProfile);
    } catch (error) {
      console.error('Failed to load user profile:', error);
    }
  }

  async loadUserPlaylists(): Promise<void> {
    try {
      this.isLoading = true;
      const response = await this.spotifyService.getUserPlaylists();
      this.userPlaylists = response.items;
      console.log(`Loaded ${this.userPlaylists.length} playlists`);
    } catch (error) {
      console.error('Failed to load playlists:', error);
    } finally {
      this.isLoading = false;
    }
  }

  async authenticateWithSpotify(): Promise<void> {
    try {
      await this.spotifyService.authorize();
    } catch (error) {
      console.error('Authentication failed:', error);
      alert('Authentication failed. Please try again.');
    }
  }

  async searchTracks(): Promise<void> {
    if (!this.searchQuery.trim()) return;
    
    this.isLoading = true;
    this.searchPerformed = true;
    this.currentView = 'search';
    
    try {
      const response = await this.spotifyService.searchTracks(this.searchQuery);
      this.searchResults = response.tracks?.items || [];
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      this.isLoading = false;
    }
  }

  async showPlaylistTracks(playlist: SpotifyPlaylist): Promise<void> {
    this.selectedPlaylistForView = playlist;
    this.currentView = 'tracks';
  }

  backToPlaylists(): void {
    this.currentView = 'playlists';
    this.selectedPlaylistForView = null;
  }

  switchToSearch(): void {
    this.currentView = 'search';
  }

  formatDuration(durationMs: number): string {
    if (!durationMs) return '0:00';
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.floor((durationMs % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

  formatDate(dateString: string): string {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }

  addToPlaylist(track: SpotifyTrack): void {
    if (!this.selectedTracks.find(t => t.id === track.id)) {
      this.selectedTracks.push(track);
    }
  }

  removeFromPlaylist(track: SpotifyTrack): void {
    this.selectedTracks = this.selectedTracks.filter(t => t.id !== track.id);
  }

  async createPlaylist(): Promise<void> {
    if (this.selectedTracks.length === 0) return;
    
    this.isLoading = true;
    
    try {
      const playlist = await this.spotifyService.createPlaylist(this.playlistName);
      this.currentPlaylist = playlist;
      const trackUris = this.selectedTracks.map(track => track.uri);
      
      await this.spotifyService.addTracksToPlaylist(playlist.id, trackUris);
      
      alert('Playlist created successfully!');
      // Refresh playlists to show the new one
      await this.loadUserPlaylists();
    } catch (error) {
      console.error('Failed to create playlist:', error);
      alert('Failed to create playlist. Please try again.');
    } finally {
      this.isLoading = false;
    }
  }

  disconnect(): void {
    this.spotifyService.disconnect();
    this.userProfile = null;
    this.userPlaylists = [];
    this.selectedTracks = [];
    this.currentPlaylist = null;
    this.currentView = 'playlists';
  }

  openInSpotify(): void {
    if (this.currentPlaylist) {
      window.open(this.currentPlaylist.external_urls.spotify, '_blank');
    }
  }

  clearPlaylist(): void {
    this.selectedTracks = [];
    this.currentPlaylist = null;
  }

  onEnterPressed(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.searchTracks();
    }
  }

  getArtistNames(artists: any[]): string {
    return artists.map(a => a.name).join(', ');
  }

  isTrackSelected(track: SpotifyTrack): boolean {
    return !!this.selectedTracks.find(t => t.id === track.id);
  }

  getAddButtonText(track: SpotifyTrack): string {
    return this.isTrackSelected(track) ? 'Added' : 'Add to Playlist';
  }
}

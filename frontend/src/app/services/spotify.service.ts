import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

export interface SpotifyTrack {
  id: string;
  name: string;
  artists: Array<{ name: string }>;
  album: { name: string };
  uri: string;
  external_urls: { spotify: string };
  preview_url?: string;
  explicit?: boolean;
  duration_ms?: number;
}

export interface SpotifyPlaylist {
  id: string;
  name: string;
  description: string;
  external_urls: { spotify: string };
  tracks: { total: number };
  owner: { display_name: string; id: string };
  public: boolean;
  collaborative: boolean;
}

export interface SpotifyUserProfile {
  country: string;
  display_name: string;
  email: string;
  explicit_content: {
    filter_enabled: boolean;
    filter_locked: boolean;
  };
  external_urls: {
    spotify: string;
  };
  followers: {
    href: string | null;
    total: number;
  };
  href: string;
  id: string;
  images: Array<{
    url: string;
    height: number | null;
    width: number | null;
  }>;
  product: string;
  type: string;
  uri: string;
}

export interface SpotifyPlaylistsResponse {
  items: SpotifyPlaylist[];
  total: number;
  limit: number;
  offset: number;
  next: string | null;
}

export interface SpotifyTracksResponse {
  items: Array<{
    track: SpotifyTrack;
    added_at: string;
  }>;
  total: number;
  limit: number;
  offset: number;
  next: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class SpotifyService {
  private clientId = '';
  private redirectUri = '';
  private scopes = [
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-read-private',
    'user-read-email',
    'playlist-modify-public',
    'playlist-modify-private'
  ];

  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  public accessToken: string | null = null;
  public refreshToken: string | null = null;

  constructor(private http: HttpClient) {
    this.loadConfig();
    this.checkTokenValidity();
  }

  private async loadConfig(): Promise<void> {
    try {
      const response = await this.http.get('/assets/config.json').toPromise() as any;
      this.clientId = response.spotify?.client_id || '';
      this.redirectUri = 'http://127.0.0.1:5001/spotify/callback';
      
      if (!this.clientId) {
        console.warn('⚠️ Spotify client ID not configured');
      }
    } catch (error) {
      console.warn('⚠️ Could not load Spotify config, using environment variables');
      // Fallback to environment variables in .env file
      this.clientId = 'bcf2215f7b7245b89fe2c40c7fb492c7'; // From your .env
      this.redirectUri = 'http://127.0.0.1:5001/spotify/callback';
    }
  }

  // Generate PKCE challenge
  private async generateCodeChallenge(codeVerifier: string): Promise<string> {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  }

  // Generate random string for PKCE
  private generateRandomString(length: number): string {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < length; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }

  // Start Spotify authorization
  async authorize(): Promise<void> {
    if (!this.clientId) {
      throw new Error('Spotify client ID not configured');
    }

    const codeVerifier = this.generateRandomString(128);
    const codeChallenge = await this.generateCodeChallenge(codeVerifier);

    // Store code verifier and return path for later use
    localStorage.setItem('spotify_code_verifier', codeVerifier);
    localStorage.setItem('spotify_return_path', window.location.pathname);

    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.clientId,
      scope: this.scopes.join(' '),
      redirect_uri: this.redirectUri,
      code_challenge_method: 'S256',
      code_challenge: codeChallenge,
    });

    window.location.href = `https://accounts.spotify.com/authorize?${params}`;
  }

  // Handle authorization callback
  async handleCallback(): Promise<boolean> {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
      const codeVerifier = localStorage.getItem('spotify_code_verifier');

      if (!codeVerifier) {
        console.error('Code verifier not found');
        return false;
      }

      try {
        const response = await fetch('http://127.0.0.1:5001/spotify/callback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            code: code,
            code_verifier: codeVerifier,
          }),
        });

        const data = await response.json();

        if (data.access_token) {
          this.accessToken = data.access_token;
          this.refreshToken = data.refresh_token;
          this.isAuthenticatedSubject.next(true);

          // Store tokens securely
          localStorage.setItem('spotify_access_token', data.access_token);
          localStorage.setItem('spotify_refresh_token', data.refresh_token);
          localStorage.setItem('spotify_token_expires', (Date.now() + (data.expires_in * 1000)).toString());

          // Clean up
          localStorage.removeItem('spotify_code_verifier');

          // Remove code from URL
          window.history.replaceState(null, '', window.location.pathname);

          return true;
        }
      } catch (error) {
        console.error('Error exchanging code for token:', error);
      }
    }
    return false;
  }

  // Refresh access token
  async refreshAccessToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('spotify_refresh_token');
    if (!refreshToken) {
      this.clearAuthData();
      return false;
    }

    try {
      const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          grant_type: 'refresh_token',
          refresh_token: refreshToken,
          client_id: this.clientId,
        }),
      });

      const data = await response.json();

      if (response.ok && data.access_token) {
        this.accessToken = data.access_token;
        localStorage.setItem('spotify_access_token', data.access_token);
        localStorage.setItem('spotify_token_expires', (Date.now() + (data.expires_in * 1000)).toString());

        if (data.refresh_token) {
          this.refreshToken = data.refresh_token;
          localStorage.setItem('spotify_refresh_token', data.refresh_token);
        }

        this.isAuthenticatedSubject.next(true);
        return true;
      } else {
        console.error('Token refresh failed:', data);
        this.clearAuthData();
        return false;
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      this.clearAuthData();
      return false;
    }
  }

  // Clear authentication data
  private clearAuthData(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('spotify_access_token');
    localStorage.removeItem('spotify_refresh_token');
    localStorage.removeItem('spotify_token_expires');
    this.isAuthenticatedSubject.next(false);
  }

  // Check if token is valid
  async checkTokenValidity(): Promise<boolean> {
    const accessToken = localStorage.getItem('spotify_access_token');
    const tokenExpires = localStorage.getItem('spotify_token_expires');

    if (!accessToken) {
      this.isAuthenticatedSubject.next(false);
      return false;
    }

    // Check if token is expired
    if (tokenExpires && Date.now() >= parseInt(tokenExpires)) {
      const refreshed = await this.refreshAccessToken();
      return refreshed;
    }

    this.accessToken = accessToken;
    this.refreshToken = localStorage.getItem('spotify_refresh_token');
    this.isAuthenticatedSubject.next(true);
    return true;
  }

  // Make authenticated Spotify API request
  private async apiRequest(endpoint: string, options: RequestInit = {}): Promise<Response> {
    if (!this.accessToken) {
      throw new Error('Not authorized');
    }

    const response = await fetch(`https://api.spotify.com/v1${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (response.status === 401) {
      // Token might be expired, try to refresh
      const refreshed = await this.refreshAccessToken();
      if (refreshed) {
        // Retry the request with new token
        return fetch(`https://api.spotify.com/v1${endpoint}`, {
          ...options,
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json',
            ...options.headers,
          },
        });
      }
      throw new Error('Authorization expired');
    }

    return response;
  }

  // Get user's playlists (all of them, including those in folders)
  async getUserPlaylists(): Promise<SpotifyPlaylistsResponse> {
    try {
      const allPlaylists: SpotifyPlaylist[] = [];
      let offset = 0;
      const limit = 50; // Maximum allowed by Spotify API
      let hasMore = true;

      while (hasMore) {
        const response = await this.apiRequest(`/me/playlists?limit=${limit}&offset=${offset}`);
        const data = await response.json();

        if (data.items && data.items.length > 0) {
          allPlaylists.push(...data.items);
          offset += limit;
          hasMore = data.next !== null; // Continue if there's a next page
        } else {
          hasMore = false;
        }
      }

      return {
        items: allPlaylists,
        total: allPlaylists.length,
        limit: limit,
        offset: 0,
        next: null
      };
    } catch (error) {
      console.error('Error fetching playlists:', error);
      throw error;
    }
  }

  // Get playlist tracks (all of them, with pagination)
  async getPlaylistTracks(playlistId: string): Promise<SpotifyTracksResponse> {
    try {
      const allTracks: Array<{ track: SpotifyTrack; added_at: string }> = [];
      let offset = 0;
      const limit = 50; // Maximum allowed by Spotify API
      let hasMore = true;

      while (hasMore) {
        const response = await this.apiRequest(`/playlists/${playlistId}/tracks?limit=${limit}&offset=${offset}`);
        const data = await response.json();

        if (data.items && data.items.length > 0) {
          allTracks.push(...data.items);
          offset += limit;
          hasMore = data.next !== null; // Continue if there's a next page
        } else {
          hasMore = false;
        }
      }

      return {
        items: allTracks,
        total: allTracks.length,
        limit: limit,
        offset: 0,
        next: null
      };
    } catch (error) {
      console.error('Error fetching playlist tracks:', error);
      throw error;
    }
  }

  // Get user profile
  async getUserProfile(): Promise<SpotifyUserProfile> {
    try {
      const response = await this.apiRequest('/me');
      return await response.json();
    } catch (error) {
      console.error('Error fetching user profile:', error);
      throw error;
    }
  }

  // Search tracks
  async searchTracks(query: string, limit: number = 20): Promise<{ tracks: { items: SpotifyTrack[] } }> {
    try {
      const response = await this.apiRequest(`/search?q=${encodeURIComponent(query)}&type=track&limit=${limit}`);
      return await response.json();
    } catch (error) {
      console.error('Error searching tracks:', error);
      throw error;
    }
  }

  // Create playlist
  async createPlaylist(name: string, description: string = '', isPublic: boolean = true): Promise<SpotifyPlaylist> {
    try {
      const userProfile = await this.getUserProfile();
      const response = await this.apiRequest(`/users/${userProfile.id}/playlists`, {
        method: 'POST',
        body: JSON.stringify({
          name,
          description,
          public: isPublic
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Error creating playlist:', error);
      throw error;
    }
  }

  // Add tracks to playlist
  async addTracksToPlaylist(playlistId: string, trackUris: string[]): Promise<any> {
    try {
      const response = await this.apiRequest(`/playlists/${playlistId}/tracks`, {
        method: 'POST',
        body: JSON.stringify({
          uris: trackUris
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Error adding tracks to playlist:', error);
      throw error;
    }
  }

  // Get stored return path and clean up
  getReturnPath(): string {
    const returnPath = localStorage.getItem('spotify_return_path') || '/spotify';
    localStorage.removeItem('spotify_return_path');
    return returnPath;
  }

  // Disconnect Spotify
  disconnect(): void {
    this.clearAuthData();
    localStorage.removeItem('spotify_return_path');
  }
}
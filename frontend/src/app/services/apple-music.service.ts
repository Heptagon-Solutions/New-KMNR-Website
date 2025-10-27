import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

// Declare MusicKit for TypeScript
declare var MusicKit: any;

@Injectable({
  providedIn: 'root'
})
export class AppleMusicService {
  private music: any;
  private isConfiguredSubject = new BehaviorSubject<boolean>(false);
  private isAuthorizedSubject = new BehaviorSubject<boolean>(false);
  
  // Backend URL
  private backendUrl = 'http://localhost:5004/api/apple-music';

  public isConfigured$ = this.isConfiguredSubject.asObservable();
  public isAuthorized$ = this.isAuthorizedSubject.asObservable();

  constructor(private http: HttpClient) {
    this.initializeMusicKit();
  }

  private async initializeMusicKit() {
    try {
      // Fetch the Developer Token from our Flask backend
      const response = await this.http.get<{ token: string }>(`${this.backendUrl}/get-developer-token`).toPromise();
      
      if (response && response.token) {
        const devToken = response.token;
        console.log('Got Apple Music Developer Token');
        
        // Configure MusicKit JS
        await this.configureMusicKit(devToken);
      }
    } catch (error) {
      console.error('Error fetching Apple Music developer token:', error);
    }
  }

  private async configureMusicKit(devToken: string) {
    try {
      await MusicKit.configure({
        developerToken: devToken,
        app: {
          name: 'KMNR Music Player',
          build: '1.0.0'
        }
      });
      
      console.log('MusicKit Configured');
      this.music = MusicKit.getInstance();
      this.isConfiguredSubject.next(true);
      
      // Check if user is already authorized
      if (this.music.isAuthorized) {
        this.isAuthorizedSubject.next(true);
      }
    } catch (error) {
      console.error('Error configuring MusicKit:', error);
    }
  }

  async login(): Promise<boolean> {
    if (!this.music) {
      console.error('MusicKit not configured');
      return false;
    }

    try {
      const userToken = await this.music.authorize();
      console.log('User authorized. User Token:', userToken);
      this.isAuthorizedSubject.next(true);
      return true;
    } catch (error) {
      console.error('Authorization failed:', error);
      return false;
    }
  }

  async logout(): Promise<void> {
    if (!this.music) return;
    
    try {
      await this.music.unauthorize();
      console.log('User unauthenticated.');
      this.isAuthorizedSubject.next(false);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }

  async search(term: string, types: string[] = ['songs'], limit: number = 10): Promise<any> {
    if (!this.music || !term) {
      throw new Error('MusicKit not configured or empty search term');
    }

    try {
      const response = await this.music.api.search(term, {
        types,
        limit
      });
      return response;
    } catch (error) {
      console.error('Search failed:', error);
      throw error;
    }
  }

  async playSong(songId: string): Promise<void> {
    if (!this.music) {
      throw new Error('MusicKit not configured');
    }

    try {
      await this.music.setQueue({ song: songId });
      await this.music.play();
      console.log(`Playing song: ${songId}`);
    } catch (error) {
      console.error('Error playing song:', error);
      throw error;
    }
  }

  async playAlbum(albumId: string): Promise<void> {
    if (!this.music) {
      throw new Error('MusicKit not configured');
    }

    try {
      await this.music.setQueue({ album: albumId });
      await this.music.play();
      console.log(`Playing album: ${albumId}`);
    } catch (error) {
      console.error('Error playing album:', error);
      throw error;
    }
  }

  async playPlaylist(playlistId: string): Promise<void> {
    if (!this.music) {
      throw new Error('MusicKit not configured');
    }

    try {
      await this.music.setQueue({ playlist: playlistId });
      await this.music.play();
      console.log(`Playing playlist: ${playlistId}`);
    } catch (error) {
      console.error('Error playing playlist:', error);
      throw error;
    }
  }

  async pause(): Promise<void> {
    if (!this.music) return;
    
    try {
      await this.music.pause();
    } catch (error) {
      console.error('Error pausing:', error);
    }
  }

  async stop(): Promise<void> {
    if (!this.music) return;
    
    try {
      await this.music.stop();
    } catch (error) {
      console.error('Error stopping:', error);
    }
  }

  async skipToNextItem(): Promise<void> {
    if (!this.music) return;
    
    try {
      await this.music.skipToNextItem();
    } catch (error) {
      console.error('Error skipping to next:', error);
    }
  }

  async skipToPreviousItem(): Promise<void> {
    if (!this.music) return;
    
    try {
      await this.music.skipToPreviousItem();
    } catch (error) {
      console.error('Error skipping to previous:', error);
    }
  }

  async getUserPlaylists(): Promise<any> {
    if (!this.music || !this.music.isAuthorized) {
      throw new Error('User not authorized');
    }

    try {
      const response = await this.music.api.music('/v1/me/library/playlists');
      return response.data.data || [];
    } catch (error) {
      console.error('Failed to get library playlists:', error);
      throw error;
    }
  }

  async getUserRecentlyPlayed(): Promise<any> {
    if (!this.music || !this.music.isAuthorized) {
      throw new Error('User not authorized');
    }

    try {
      const response = await this.music.api.music('/v1/me/recent/played');
      return response.data.data || [];
    } catch (error) {
      console.error('Failed to get recently played:', error);
      throw error;
    }
  }

  isConfigured(): boolean {
    return this.isConfiguredSubject.value;
  }

  isAuthorized(): boolean {
    return this.isAuthorizedSubject.value;
  }

  getCurrentPlayer(): any {
    return this.music;
  }
}
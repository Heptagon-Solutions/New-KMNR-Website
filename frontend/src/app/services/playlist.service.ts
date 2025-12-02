import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PlaylistProfile, Track } from 'src/models/playlist';

@Injectable({
  providedIn: 'root'
})
export class PlaylistService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {
    this.detectBackendPort();
  }

  private async detectBackendPort(): Promise<void> {
    const ports = [5000, 5001, 5002];
    
    for (const port of ports) {
      try {
        const testUrl = `http://127.0.0.1:${port}/test`;
        await this.http.get(testUrl, { withCredentials: true }).toPromise();
        this.baseUrl = `http://127.0.0.1:${port}`;
        console.log(`✅ Found backend on port ${port}`);
        return;
      } catch (error) {
        // Port not available, try next
      }
    }
    
    console.warn('⚠️ Could not detect backend port, using default 5000');
  }

  getPlaylists(djId?: number): Observable<PlaylistProfile[]> {
    let params: any = {};
    if (djId) {
      params.dj_id = djId.toString();
    }
    return this.http.get<PlaylistProfile[]>(`${this.baseUrl}/playlists`, {
      params,
      withCredentials: true
    });
  }

  getPlaylistTracks(playlistId: number): Observable<Track[]> {
    return this.http.get<Track[]>(`${this.baseUrl}/playlists/${playlistId}/tracks`, {
      withCredentials: true
    });
  }

  publishToSpotify(playlistId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/playlists/${playlistId}/publish-to-spotify`, {}, {
      withCredentials: true
    });
  }
}
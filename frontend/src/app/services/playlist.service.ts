import { Injectable } from '@angular/core';

import { PlaylistEntry, Playlist } from '../../models';

const URL = 'http://localhost:8971/playlist/';

const SAMPLE_PLAYLIST: PlaylistEntry[] = [
  { 
    id: 1, 
    artist: "The Strokes", 
    title: "Last Nite", 
    album: "Is This It", 
    genre: "Indie Rock", 
    played_at: "2024-12-14T10:30:00Z", 
    dj_name: "Indie Isaac" 
  },
  { 
    id: 2, 
    artist: "Led Zeppelin", 
    title: "Stairway to Heaven", 
    album: "Led Zeppelin IV", 
    genre: "Classic Rock", 
    played_at: "2024-12-14T10:15:00Z", 
    dj_name: "Mining Mike" 
  },
  { 
    id: 3, 
    artist: "Daft Punk", 
    title: "One More Time", 
    album: "Discovery", 
    genre: "Electronic", 
    played_at: "2024-12-14T10:00:00Z", 
    dj_name: "Techno Tyler" 
  },
  { 
    id: 4, 
    artist: "Miles Davis", 
    title: "Kind of Blue", 
    album: "Kind of Blue", 
    genre: "Jazz", 
    played_at: "2024-12-14T09:45:00Z", 
    dj_name: "Jazz Jessica" 
  },
  { 
    id: 5, 
    artist: "Metallica", 
    title: "Enter Sandman", 
    album: "Metallica", 
    genre: "Heavy Metal", 
    played_at: "2024-12-14T09:30:00Z", 
    dj_name: "Metal Miner" 
  },
  { 
    id: 6, 
    artist: "Taylor Swift", 
    title: "Anti-Hero", 
    album: "Midnights", 
    genre: "Pop", 
    played_at: "2024-12-14T09:15:00Z", 
    dj_name: "Pop Princess" 
  },
  { 
    id: 7, 
    artist: "Johnny Cash", 
    title: "Ring of Fire", 
    album: "Ring of Fire: The Best of Johnny Cash", 
    genre: "Country", 
    played_at: "2024-12-14T09:00:00Z", 
    dj_name: "Country Chris" 
  },
  { 
    id: 8, 
    artist: "Radiohead", 
    title: "Creep", 
    album: "Pablo Honey", 
    genre: "Alternative", 
    played_at: "2024-12-14T08:45:00Z", 
    dj_name: "Indie Isaac" 
  },
  { 
    id: 9, 
    artist: "Bon Iver", 
    title: "Holocene", 
    album: "Bon Iver, Bon Iver", 
    genre: "Indie Folk", 
    played_at: "2024-12-14T08:30:00Z", 
    dj_name: "Ambient Adam" 
  },
  { 
    id: 10, 
    artist: "The Ramones", 
    title: "Blitzkrieg Bop", 
    album: "Ramones", 
    genre: "Punk", 
    played_at: "2024-12-14T08:15:00Z", 
    dj_name: "Punk Pete" 
  }
];

@Injectable({
  providedIn: 'root',
})
export class PlaylistService {
  constructor() {}

  public async getRecentTracks(limit: number = 50): Promise<PlaylistEntry[]> {
    console.log('🌐 DEBUG: Fetching from URL:', URL + `recent?limit=${limit}`);
    try {
      const data = await fetch(URL + `recent?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        mode: 'cors'
      });
      console.log('📡 DEBUG: Fetch response:', { status: data.status, ok: data.ok, statusText: data.statusText });
      if (data.ok) {
        const result = await data.json();
        console.log('✅ DEBUG: API returned data:', { count: result.length, first: result[0] });
        return result;
      } else {
        console.log('❌ DEBUG: API response not ok, status:', data.status, data.statusText);
      }
    } catch (error) {
      console.log('❌ DEBUG: Fetch error (likely CORS), using sample data:', error);
    }
    console.log('📋 DEBUG: Returning sample data, count:', SAMPLE_PLAYLIST.slice(0, limit).length);
    return SAMPLE_PLAYLIST.slice(0, limit);
  }

  public async getTracksByDJ(djId: number): Promise<PlaylistEntry[]> {
    try {
      const data = await fetch(URL + `dj/${djId}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Using sample playlist data');
    }
    return SAMPLE_PLAYLIST.filter(track => track.dj_name.includes(djId.toString()));
  }

  public async getPlaylistsByDJ(djId: number): Promise<Playlist[]> {
    try {
      const data = await fetch(URL + `by-dj/${djId}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Error fetching playlists by DJ, using fallback');
    }
    return [];
  }

  public async getAllPlaylists(): Promise<Playlist[]> {
    try {
      const data = await fetch(URL + 'all');
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Error fetching all playlists, using fallback');
    }
    return [];
  }

  public async getPlaylistDetails(playlistId: number): Promise<any> {
    try {
      const data = await fetch(URL + `${playlistId}`);
      if (data.ok) {
        return await data.json();
      }
    } catch (error) {
      console.log('Error fetching playlist details');
    }
    return null;
  }
}
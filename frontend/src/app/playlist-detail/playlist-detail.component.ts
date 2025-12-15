import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { PlaylistService } from '../services/playlist.service';

interface PlaylistDetail {
  id: number;
  name: string;
  description?: string;
  date_played: string;
  dj_id: number;
  dj_name: string;
  tracks: {
    track_number: number;
    title: string;
    artist: string;
    album: string;
  }[];
}

@Component({
  selector: 'app-playlist-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './playlist-detail.component.html',
  styleUrls: ['./playlist-detail.component.scss']
})
export class PlaylistDetailComponent implements OnInit {
  playlist: PlaylistDetail | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private playlistService: PlaylistService
  ) {}

  async ngOnInit() {
    console.log('🎵 DEBUG: Playlist Detail component initializing...');
    
    this.route.params.subscribe(async params => {
      const playlistId = +params['id'];
      console.log('🆔 DEBUG: Loading playlist with ID:', playlistId);
      
      await this.loadPlaylist(playlistId);
    });
  }

  async loadPlaylist(playlistId: number) {
    try {
      this.playlist = await this.playlistService.getPlaylistDetails(playlistId);
      
      if (this.playlist) {
        console.log('✅ DEBUG: Playlist loaded:', {
          id: playlistId,
          name: this.playlist.name,
          tracks: this.playlist.tracks.length,
          dj: this.playlist.dj_name
        });
      } else {
        this.error = 'Playlist not found';
        console.log('❌ DEBUG: Playlist not found for ID:', playlistId);
      }
    } catch (error) {
      console.error('❌ DEBUG: Error loading playlist:', error);
      this.error = 'Error loading playlist';
    } finally {
      this.loading = false;
    }
  }

  goBack() {
    this.router.navigate(['/playlists']);
  }

  viewDJProfile() {
    if (this.playlist?.dj_id) {
      this.router.navigate(['/djs', this.playlist.dj_id]);
    }
  }

  formatPlayedTime(playedAt: string): string {
    if (!playedAt) return 'Unknown time';
    const date = new Date(playedAt);
    return date.toLocaleDateString();
  }
}
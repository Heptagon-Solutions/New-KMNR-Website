import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { PlaylistService } from '../services/playlist.service';
import { Playlist } from '../../models';

@Component({
  selector: 'app-dj-playlist',
  standalone: true,
  imports: [CommonModule, RouterModule],
  providers: [PlaylistService],
  templateUrl: './dj-playlist.component.html',
  styleUrls: ['./dj-playlist.component.scss']
})
export class DJPlaylistComponent implements OnInit {
  playlists: Playlist[] = [];
  loading = false;

  constructor(
    private playlistService: PlaylistService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  async ngOnInit(): Promise<void> {
    await this.loadPlaylists();
  }

  async loadPlaylists(): Promise<void> {
    console.log('🔍 DEBUG: Starting to load playlists...');
    this.loading = true;
    try {
      this.playlists = await this.playlistService.getAllPlaylists();
      console.log('✅ DEBUG: Loaded playlists:', this.playlists.length);
    } catch (error) {
      console.error('❌ DEBUG: Failed to load playlists:', error);
    } finally {
      this.loading = false;
      this.cdr.detectChanges();
    }
  }

  formatPlayedTime(playedAt: string): string {
    if (!playedAt) return 'Unknown time';
    const date = new Date(playedAt);
    return date.toLocaleDateString();
  }

  trackByFn(index: number, playlist: any): any {
    return playlist.id;
  }

  getDJCount(): number {
    const uniqueDJs = new Set(this.playlists.map(playlist => playlist.dj_name));
    return uniqueDJs.size;
  }

  viewPlaylist(playlist: Playlist): void {
    this.router.navigate(['/playlist', playlist.id]);
  }

  viewDJProfile(playlist: Playlist): void {
    this.router.navigate(['/djs', playlist.dj_id]);
  }
}
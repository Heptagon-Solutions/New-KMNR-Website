import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { DJService } from '../shared/dj.service';
import { PlaylistService } from '../services/playlist.service';
import { DJ, Playlist } from '../../models';

@Component({
  selector: 'app-dj-profile-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dj-profile-detail.component.html',
  styleUrls: ['./dj-profile-detail.component.scss']
})
export class DjProfileDetailComponent implements OnInit {
  dj: DJ | null = null;
  djPlaylists: Playlist[] = [];
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private djService: DJService,
    private playlistService: PlaylistService
  ) {}

  async ngOnInit() {
    console.log('🎧 DEBUG: DJ Profile component initializing...');
    
    this.route.params.subscribe(async params => {
      const djId = +params['id'];
      console.log('🆔 DEBUG: Loading DJ with ID:', djId);
      
      await this.loadDJProfile(djId);
      await this.loadDJPlaylists(djId);
    });
  }

  async loadDJProfile(djId: number) {
    try {
      this.dj = await this.djService.getDJ(djId);
      console.log('✅ DEBUG: DJ loaded:', this.dj);
    } catch (error) {
      console.error('❌ DEBUG: Error loading DJ:', error);
      this.error = 'DJ not found';
    }
  }

  async loadDJPlaylists(djId: number) {
    try {
      this.djPlaylists = await this.playlistService.getPlaylistsByDJ(djId);
      console.log('🎵 DEBUG: DJ playlists loaded:', this.djPlaylists.length);
    } catch (error) {
      console.error('❌ DEBUG: Error loading DJ playlists:', error);
    } finally {
      this.loading = false;
    }
  }

  goBack() {
    this.router.navigate(['/djs']);
  }

  formatPlayedTime(playedAt: string): string {
    if (!playedAt) return 'Unknown time';
    const date = new Date(playedAt);
    return date.toLocaleDateString();
  }

  viewPlaylist(playlist: Playlist) {
    this.router.navigate(['/playlist', playlist.id]);
  }
}
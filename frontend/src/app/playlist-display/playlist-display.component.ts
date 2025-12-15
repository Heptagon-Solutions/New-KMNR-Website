import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SpotifyService, SpotifyPlaylist, SpotifyTracksResponse, SpotifyTrack } from '../services/spotify.service';

@Component({
  selector: 'playlist-display',
  standalone: true,
  imports: [CommonModule],
  providers: [SpotifyService],
  templateUrl: './playlist-display.component.html',
  styleUrls: ['./playlist-display.component.scss']
})
export class PlaylistDisplayComponent implements OnInit, OnChanges {
  @Input() playlistId: string | null = null;
  @Input() showEmbed: boolean = false;
  @Input() embedHeight: string = '352px';

  playlistDetails: SpotifyPlaylist | null = null;
  playlistTracks: Array<{ track: SpotifyTrack; added_at: string }> = [];
  isLoading = false;
  errorMessage: string | null = null;

  constructor(private spotifyService: SpotifyService) {}

  ngOnInit(): void {
    if (this.playlistId) {
      this.loadPlaylistData();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['playlistId'] && !changes['playlistId'].firstChange) {
      this.loadPlaylistData();
    }
  }

  getEmbedUrl(): string {
    if (!this.playlistId) return '';
    return `https://open.spotify.com/embed/playlist/${this.playlistId}?utm_source=generator`;
  }

  async loadPlaylistData(): Promise<void> {
    if (!this.playlistId) {
      this.errorMessage = 'No Playlist ID provided.';
      this.playlistDetails = null;
      this.playlistTracks = [];
      return;
    }

    if (!this.spotifyService.accessToken) {
       this.errorMessage = 'Spotify is not authenticated.';
       return;
    }

    this.isLoading = true;
    this.errorMessage = null;
    this.playlistDetails = null;
    this.playlistTracks = [];

    try {
      this.playlistDetails = await this.spotifyService.getPlaylist(this.playlistId);
      const tracksResponse: SpotifyTracksResponse = await this.spotifyService.getPlaylistTracks(this.playlistId);
      this.playlistTracks = tracksResponse.items.filter(item => item.track);

    } catch (error: any) {
      console.error('Error loading playlist data:', error);
      this.errorMessage = error.message || 'Failed to load playlist data. Ensure Spotify is connected and the ID is correct.';
    } finally {
      this.isLoading = false;
    }
  }

  getArtistNames(artists: Array<{ name: string }> | undefined): string {
    if (!artists) return 'Unknown Artist';
    return artists.map(a => a.name).join(', ');
  }

  formatDuration(durationMs: number | undefined): string {
    if (durationMs === undefined) return '--:--';
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.floor((durationMs % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

   formatDate(dateString: string | undefined): string {
    if (!dateString) return 'Unknown date';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    } catch {
      return 'Invalid date';
    }
  }

  openInSpotify(): void {
    if (this.playlistDetails?.external_urls?.spotify) {
      window.open(this.playlistDetails.external_urls.spotify, '_blank');
    }
  }
}

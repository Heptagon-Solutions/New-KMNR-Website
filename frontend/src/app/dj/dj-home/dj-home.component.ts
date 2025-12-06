import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DayOfTheWeek } from 'src/models/general';
import { PlaylistProfile } from 'src/models/playlist';
import { Show } from 'src/models/show';
import { DJ } from 'src/models/dj';
import { SpotifyService } from 'src/app/services/spotify.service';
import { PlaylistService } from 'src/app/services/playlist.service';

const SAMPLE_DJ: DJ = {
  id: 1,
  djName: 'A DJ',
  userName: 'Real name',
  profileImg: null,
};

const SAMPLE_SHOWS: Show[] = [
  {
    id: 1,
    name: "Baby's First Show",
    shortDesc: 'dummy show data',
    day: DayOfTheWeek.Friday,
    startTime: 14,
    endTime: 15,
    semester: {
      term: 'Fall',
      year: 2025,
    },
    hosts: [SAMPLE_DJ],
  },
];

const SAMPLE_PLAYLISTS: PlaylistProfile[] = [
  {
    id: 1,
    datePlayed: '2025-10-1 13:45:13',
    name: "Baby's first playlist",
    hidden: false,
    author: SAMPLE_DJ,
    show: null,
    spotifyPlaylistId: null,
    description: 'This is test data for a playlist object',
  },
];

@Component({
  selector: 'dj-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dj-home.component.html',
  styleUrls: ['./dj-home.component.scss'],
})
export class DJHomeComponent implements OnInit {
  protected shows: Show[] = [];
  protected loadingShows: boolean = true;

  protected isSpotifyConnected: boolean = false;

  protected playlists: PlaylistProfile[] = [];
  protected loadingPlaylists: boolean = true;

  constructor(
    private readonly spotifyService: SpotifyService,
    private readonly playlistService: PlaylistService
  ) {}

  public ngOnInit() {
    this.spotifyService.isAuthenticated$.subscribe(isAuth => {
      this.isSpotifyConnected = isAuth;
    });

    this.loadShows();
    this.loadPlaylists();
  }

  public loadShows() {
    console.debug(
      'Loading dummy show data since there is no proper ShowService methods yet...'
    );
    this.shows = SAMPLE_SHOWS;
    this.loadingShows = false;
  }

  public connectToSpotify() {
    this.spotifyService.authorize();
  }

  public loadPlaylists() {
    if (!this.isSpotifyConnected) {
      console.debug(
        "Loading dummy playlist data since Spotify isn't connected..."
      );
      this.playlists = SAMPLE_PLAYLISTS;
      this.loadingPlaylists = false;
    } else {
      this.loadingPlaylists = true;
      this.playlistService.getPlaylists().subscribe({
        next: playlists => {
          this.playlists = playlists;
          this.loadingPlaylists = false;
        },
        error: error => {
          console.error('Failed to load playlists:', error);
          this.loadingPlaylists = false;
        },
      });
    }
  }

  public publishToSpotify(playlist: PlaylistProfile) {
    if (!this.isSpotifyConnected) {
      alert('Please connect to Spotify first');
      return;
    }

    this.playlistService.publishToSpotify(playlist.id).subscribe({
      next: response => {
        playlist.spotifyPlaylistId = response.spotify_playlist_id;
        alert(
          `Playlist published to Spotify! ${response.tracks_added} tracks added.`
        );

        if (response.spotify_url) {
          window.open(response.spotify_url, '_blank');
        }
      },
      error: error => {
        console.error('Failed to publish playlist:', error);
        alert('Failed to publish playlist to Spotify');
      },
    });
  }

  public openSpotifyPlaylist(spotifyPlaylistId: string) {
    if (spotifyPlaylistId) {
      window.open(
        `https://open.spotify.com/playlist/${spotifyPlaylistId}`,
        '_blank'
      );
    }
  }
}

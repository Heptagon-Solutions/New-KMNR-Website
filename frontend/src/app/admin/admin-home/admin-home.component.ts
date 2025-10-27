import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { PlaylistService } from '../../services/playlist.service';

@Component({
  selector: 'app-admin-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.scss'],
})
export class AdminHomeComponent implements OnInit {
  playlists: any[] = [];
  isLoading = false;

  constructor(
    private playlistService: PlaylistService
  ) {}

  ngOnInit() {
    this.loadPlaylists();
  }

  loadPlaylists() {
    this.isLoading = true;
    this.playlistService.getPlaylists().subscribe({
      next: (playlists) => {
        this.playlists = playlists;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load playlists:', error);
        this.isLoading = false;
      }
    });
  }
}
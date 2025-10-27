import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SpotifyPlayerComponent } from '../spotify-player/spotify-player.component';

@Component({
  selector: 'app-player-page',
  standalone: true,
  imports: [CommonModule, SpotifyPlayerComponent],
  templateUrl: './player-page.component.html',
  styleUrls: ['./player-page.component.css']
})
export class PlayerPageComponent {
  
}
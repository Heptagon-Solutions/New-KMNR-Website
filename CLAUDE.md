# Apple Music & Spotify Integration Reference

## Apple Music Component Reference

## Core Component Code
```typescript
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, Renderer2, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';

// This must match the declaration in main.ts
declare var MusicKit: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'My Apple Music App';
  music: any; // This will hold the MusicKit instance
  
  // State for search and playlists
  public searchResults: any[] = [];
  public myPlaylists: any[] = [];
  
  // --- New Theme Properties ---
  public isSpotifyTheme = false;
  // --------------------------
  
  // Backend URL
  private backendUrl = 'http://localhost:5000/api/get-developer-token';
  
  constructor(
    private http: HttpClient,
    // --- New Injections for Theme Toggle ---
    private renderer: Renderer2,
    @Inject(DOCUMENT) private document: Document
    // -------------------------------------
  ) {}
  
  ngOnInit(): void {
    // 1. Fetch the Developer Token from our Flask Backend
    this.http.get<{ token: string }>(this.backendUrl).subscribe(
      (res) => {
        const devToken = res.token;
        console.log('Got Developer Token');
        
        // 2. Configure MusicKit JS
        this.configureMusicKit(devToken);
      },
      (err) => {
        console.error('Error fetching developer token:', err);
      }
    );
  }
  
  private async configureMusicKit(devToken: string) {
    try {
      await MusicKit.configure({
        developerToken: devToken,
        app: {
          name: 'My Cool Web App',
          build: '1.0.0'
        }
      });
      console.log('MusicKit Configured');
      this.music = MusicKit.getInstance();
    } catch (err) {
      console.error('Error configuring MusicKit:', err);
    }
  }
  
  // --- New Theme Toggle Method ---
  toggleTheme(): void {
    this.isSpotifyTheme = !this.isSpotifyTheme;
    if (this.isSpotifyTheme) {
      this.renderer.addClass(this.document.body, 'theme-spotify');
    } else {
      this.renderer.removeClass(this.document.body, 'theme-spotify');
    }
  }
  // -----------------------------
  
  async login() {
    if (!this.music) return;
    try {
      // This line shows the Apple login popup
      const userToken = await this.music.authorize();
      console.log('User authorized. User Token:', userToken);
    } catch (err) {
      console.error('Authorization failed:', err);
    }
  }
  
  async logout() {
    if (!this.music) return;
    await this.music.unauthorize();
    console.log('User unauthenticated.');
    // Clear user-specific data
    this.myPlaylists = [];
  }
  
  async search(term: string) {
    if (!this.music || !term) return;
    
    try {
      const response = await this.music.api.search(term, {
        types: ['songs'],
        limit: 10
      });
      
      this.searchResults = response.songs?.data || [];
      console.log('Search results:', this.searchResults);
    } catch (err) {
      console.error('Search failed:', err);
      this.searchResults = [];
    }
  }
  
  async playSong(songId: string) {
    if (!this.music) return;
    
    try {
      // This queues the song and starts playbook
      await this.music.setQueue({ song: songId });
      await this.music.play();
      console.log(`Playing song: ${songId}`);
    } catch (err) {
      console.error('Error playing song:', err);
    }
  }
  
  async getMyPlaylists() {
    // This call automatically uses the Music User Token
    // It will fail if the user is not logged in
    if (!this.music || !this.music.isAuthorized) {
      console.error('User not authorized to fetch playlists.');
      return;
    }
    
    try {
      const response = await this.music.api.library.playlists();
      this.myPlaylists = response.data || [];
      console.log('User playlists:', this.myPlaylists);
    } catch (err) {
      console.error('Failed to get library playlists:', err);
      this.myPlaylists = [];
    }
  }
}
```

## Key Features
- MusicKit JS integration with developer token from Flask backend
- Apple Music authentication (login/logout)
- Song search functionality
- Playlist retrieval from user's library
- Song playback controls
- Theme toggle between default and Spotify styling
- Error handling for all music operations

## Backend Integration
- Fetches developer token from `http://localhost:5000/api/get-developer-token`
- Requires Flask backend to provide Apple Music developer token

## Dependencies
- Angular HttpClient for API calls
- Angular Renderer2 and DOCUMENT for theme management
- MusicKit JS library (must be declared globally)

## HTML Template (app.component.html)
```html
<!-- src/app/app.component.html -->
<div class="app-container">
  <!-- Theme Toggle Button -->
  <button 
    class="theme-toggle-btn"
    [class.spotify-btn]="!isSpotifyTheme"
    [class.apple-btn]="isSpotifyTheme"
    (click)="toggleTheme()">
    {{ isSpotifyTheme ? 'Switch to Apple Theme' : 'Switch to Spotify Theme' }}
  </button>

  <h1>{{ title }}</h1>
  
  <!-- Show login button if not logged in -->
  <button *ngIf="music && !music.isAuthorized" (click)="login()">
    Login to Apple Music
  </button>

  <!-- Show welcome message if logged in -->
  <div *ngIf="music && music.isAuthorized">
    <p>Welcome, you are logged in!</p>
    <button (click)="logout()">Logout</button>
  </div>
</div>

<div class="app-container" style="margin-top: 0;">
  <!-- Search Section -->
  <h3>Search for a Song</h3>
  <input #searchInput type="text" (keyup.enter)="search(searchInput.value)" placeholder="Enter song name...">
  <button (click)="search(searchInput.value)">Search</button>

  <div *ngIf="searchResults.length > 0">
    <h4>Results:</h4>
    <ul>
      <li *ngFor="let song of searchResults">
        <span>
          <strong>{{ song.attributes.name }}</strong> 
          by {{ song.attributes.artistName }}
        </span>
        <!-- Add a play button -->
        <button (click)="playSong(song.id)">
          Play
        </button>
      </li>
    </ul>
  </div>
</div>

<!-- Library Playlists Section -->
<div class="app-container" style="margin-top: 0;" *ngIf="music && music.isAuthorized">
  <h3>My Library</h3>
  <button (click)="getMyPlaylists()">Get My Playlists</button>
  <ul *ngIf="myPlaylists.length > 0">
    <li *ngFor="let playlist of myPlaylists">
      {{ playlist.attributes.name }}
    </li>
  </ul>
</div>
```

## CSS Styles (app.component.css)
```css
/* src/app/app.component.css */

/* Main container for the app */
.app-container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
  background-color: var(--secondary-background-color);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--border-color);
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

h1 {
  color: var(--text-color);
  border-bottom: 2px solid var(--primary-accent-color);
  padding-bottom: 10px;
  display: inline-block;
}

h3 {
  color: var(--text-color);
  margin-top: 30px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 5px;
}

p, label {
  color: var(--text-color-light);
}

/* Standard Button Styling */
button {
  background-color: var(--primary-accent-color);
  color: var(--primary-accent-text-color);
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 5px;
}

button:hover {
  filter: brightness(1.15);
  transform: scale(1.02);
}

button:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

/* Theme Toggle Button */
.theme-toggle-btn {
  display: block;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  position: absolute;
  top: 30px;
  right: 40px;
}

/* Specific theme styles for the toggle button itself */
.theme-toggle-btn.apple-btn {
  background-color: #fa5050; /* Apple Red */
  color: #ffffff;
}
.theme-toggle-btn.spotify-btn {
  background-color: #1db954; /* Spotify Green */
  color: #ffffff;
}

/* Input Field Styling */
input[type="text"] {
  width: calc(100% - 110px);
  padding: 12px;
  font-size: 16px;
  border-radius: 25px;
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color);
  margin-right: 10px;
}

input[type="text"]:focus {
  outline: none;
  border-color: var(--primary-accent-color);
  box-shadow: 0 0 5px var(--primary-accent-color);
}

/* Results List Styling */
ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 10px;
}

li button {
  font-size: 14px;
  padding: 8px 14px;
  margin: 0;
}
```

## Global Styles (styles.css)
```css
/* src/styles.css */

/* We define all our colors as CSS variables.
  :root contains the default theme (Apple Music). */
:root {
  --background-color: #ffffff;
  --text-color: #1d1d1f;
  --text-color-light: #515154;
  --primary-accent-color: #fa5050;
  --primary-accent-text-color: #ffffff;
  --secondary-background-color: #f5f5f7;
  --border-color: #d2d2d7;

  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* When the body has the 'theme-spotify' class,
  we override all the variables with Spotify's colors. */
body.theme-spotify {
  --background-color: #121212;
  --text-color: #ffffff;
  --text-color-light: #b3b3b3;
  --primary-accent-color: #1db954;
  --primary-accent-text-color: #ffffff;
  --secondary-background-color: #282828;
  --border-color: #404040;
}

/* Global body styles that use the variables */
body {
  margin: 0;
  padding: 0;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

## Spotify Integration Tutorial Notes

### Key Issues to Solve:
- Missing methods in Angular SpotifyService (.playTrack(), .nextTrack(), etc.)
- Type mismatches: Components expect arrays but get full API response objects
- Need proper unwrapping of Spotify API responses

### Angular Service Structure:
```typescript
export interface SpotifyTrack {
  id: string;
  name: string;
  uri: string;
}

export interface SpotifyPlaylist {
  id: string;
  name: string;
}

export interface SpotifySearchResponse {
  tracks: { items: SpotifyTrack[]; };
}

export interface SpotifyPlaylistsResponse {
  items: SpotifyPlaylist[];
}
```

### Flask Backend Routes Needed:
- POST /api/spotify/play
- POST /api/spotify/pause
- POST /api/spotify/resume
- POST /api/spotify/next
- POST /api/spotify/previous
- GET /api/spotify/search
- GET /api/spotify/playlists

### Component Fixes:
- Assign `results.tracks.items` not `results` to searchResults
- Assign `results.items` not `results` to userPlaylists
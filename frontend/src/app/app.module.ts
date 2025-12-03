import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './shared/top-bar/top-bar.component';
import { FooterComponent } from './shared/footer/footer.component';
import { SpotifyPlaylistComponent } from './spotify-playlist/spotify-playlist.component';
import { SpotifyCallbackComponent } from './spotify-callback/spotify-callback.component';
import { PlaylistDisplayComponent } from './playlist-display/playlist-display.component';
import { WebstreamPlayerComponent } from './shared/webstream-player/webstream-player.component';

@NgModule({
  declarations: [
    AppComponent,
    SpotifyPlaylistComponent,
    SpotifyCallbackComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    TopBarComponent,
    FooterComponent,
    PlaylistDisplayComponent,
    WebstreamPlayerComponent,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}

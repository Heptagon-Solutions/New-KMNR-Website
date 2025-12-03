import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './shared/top-bar/top-bar.component';
import { FooterComponent } from './shared/footer/footer.component';
import { SpotifyService } from './services/spotify.service';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    TopBarComponent,
    FooterComponent
  ],
  providers: [SpotifyService],
  bootstrap: [AppComponent],
})
export class AppModule {}

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { BlogComponent } from './blog/blog.component';
import { AboutComponent } from './about/about.component';
import { NewsComponent } from './news/news.component';
import { NewsFormComponent } from './news/news-form/news-form.component';
import { DJListComponent } from './dj-list/dj-list.component';
import { DJProfileComponent } from './dj-list/dj-profile/dj-profile.component';
import { ShowsComponent } from './shows/shows.component';
import { AdminHomeComponent } from './admin/admin-home/admin-home.component';
import { AdminNewsComponent } from './admin/admin-news/admin-news.component';
import { PlayerPageComponent } from './player-page/player-page.component';
import { AppleMusicPlayerComponent } from './apple-music-player/apple-music-player.component';
import { SpotifyPlayerComponent } from './spotify-player/spotify-player.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'shows',
    component: ShowsComponent,
  },
  {
    path: 'djs',
    children: [
      {
        path: '',
        component: DJListComponent,
      },
      {
        path: ':id',
        component: DJProfileComponent,
      },
    ],
  },
  {
    path: 'news',
    children: [
      {
        path: '',
        component: NewsComponent,
      },
      {
        path: 'form',
        component: NewsFormComponent,
      },
    ],
  },
  {
    path: 'about',
    component: AboutComponent,
  },
  {
    path: 'blog',
    component: BlogComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'player',
    component: PlayerPageComponent,
  },
  {
    path: 'apple-music',
    component: AppleMusicPlayerComponent,
  },
  {
    path: 'spotify',
    component: SpotifyPlayerComponent,
  },
  {
    // TO DO: AUTHENTICATION HERE
    path: 'admin',
    children: [
      {
        path: '',
        component: AdminHomeComponent,
      },
      {
        path: 'news',
        component: AdminNewsComponent,
      },
    ],
  },
  {
    path: '**',
    redirectTo: '',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

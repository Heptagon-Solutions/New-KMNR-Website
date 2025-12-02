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
import { AdminUsersComponent } from './admin/admin-users/admin-users.component';
import { AdminDJsComponent } from './admin/admin-djs/admin-djs.component';
import { SpotifyPlaylistComponent } from './spotify-playlist/spotify-playlist.component';
import { SpotifyCallbackComponent } from './spotify-callback/spotify-callback.component';

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
    path: 'spotify',
    component: SpotifyPlaylistComponent,
  },
  {
    path: 'callback',
    component: SpotifyCallbackComponent,
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
      {
        path: 'users',
        component: AdminUsersComponent,
      },
      {
        path: 'djs',
        component: AdminDJsComponent,
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

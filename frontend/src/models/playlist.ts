import { DJ } from './dj';
import { Show } from './show';

export interface Track {
  trackNum: number;
  song: string;
  artist: string;
  album?: string;
}

export interface Playlist {
  id: number;
  datePlayed: string; // Or some kind of Datetime type?
  name?: string;
  hidden: boolean;
  author: DJ; // Or should this just only be for the profile?
  show: Show | null; // Should this just be an id instead?
  spotifyPlaylistId: string | null;
  // image?
}

export interface PlaylistProfile extends Playlist {
  description?: string;
  // image?
}

/*
export interface PlaylistTrack {
  track: number;
  song: string;
  artist: string;
  album?: string;
}

export interface Playlist {
  id: number;
  name?: string;
  description?: string;
  date_played: string;
  spotify_playlist_id?: string;
  dj_name?: string;
  posting_dj_id?: number;
}
*/

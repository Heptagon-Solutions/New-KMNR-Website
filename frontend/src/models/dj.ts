export interface DJ {
  id: number;
  djName: string;
  userName: string;
  // genres: string; // Will we have genres for DJs? Not currently supported by DB
  /** The URL path to the DJ's profile image, scheme and domain not included (ex: '/api/djs/1/profile-image') */
  profileImg: string | null;
}

export interface DJProfile extends DJ {
  profileDesc: string;
}

export interface DJ {
  id: number;
  djName: string;
  userName: string;
  // genres: string; // Will we have genres for DJs? Not currently supported by DB
  profileImg: string | null;
}

export interface DJProfile extends DJ {
  profileDesc: string;
  // profileImg: Blob;  // TODO: learn more about how we'll handle images
}

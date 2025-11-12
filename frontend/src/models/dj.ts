export interface DJ {
  id: number;
  djName: string;
  // genres: string; // Will we have genres for DJs? Not currently supported by DB
  // profile image here or in DJProfile?
}

export interface DJProfile extends DJ {
  desc: string;
  // profileImg: Blob;  // TODO: learn more about how we'll handle images
}

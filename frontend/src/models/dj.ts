export interface DJ {
  id: number;
  name: string;
  genres: string;
  // profile image here or in DJProfile?
}

export interface DJProfile extends DJ {
  desc: string;
  image: Blob;
}

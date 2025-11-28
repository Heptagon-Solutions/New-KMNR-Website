export interface Semester {
  term: string;
  year: number;
}

export interface DJ {
  id: number;
  name: string;
  genres: string;
  show?: string;
}

export interface TownAndCampusNewsEntry {
  title: string;
  location: string;
  contact_email: string;
  description: string;
}

export interface TownAndCampusNewsEntryDetailed {
  id: number;
  title: string;
  organization: string;
  description: string;
  location: string;
  website: string;
  contact_name: string;
  contact_email: string;
  approved: boolean;
  submit_date: string; // ??? Date object instead ???
  expiration_date: string; // ^
}

export interface ContactInfo {
  twitter: string;
  email: string;
  phoneNumbers: {
    request: string;
    office: string;
    texter: string;
  };
  address: {
    line1: string;
    line2: string;
    cityStateZip: string;
  };
}

export interface ExecutiveBoard {
  stationManager: string;
  programDirector: string;
  chiefEngineer: string;
  personnelDirector: string;
  businessDirector: string;
  publicRelations: string;
  musicDirector: string;
  roadshowDirectors: string;
  newsDirector: string;
  productions: string;
  historian: string;
}

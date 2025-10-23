export interface TownAndCampusNewsEntry {
  id: number;
  title: string;
  approved: boolean;
  submitDate: string; // ??? Date object instead ???
  expirationDate: string; // ^
}

export interface TownAndCampusNewsEntryDetailed extends TownAndCampusNewsEntry {
  organization: string;
  description: string;
  location: string;
  website: string;
  contactName: string;
  contactEmail: string;
}

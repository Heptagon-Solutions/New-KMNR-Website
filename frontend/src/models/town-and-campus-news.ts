export interface TownAndCampusNewsEntryFormData {
  title: string;
  description: string;
  location: string;
  contactName: string;
  contactEmail: string;
  expirationDate: string | null;
  organization: string | null;
  website: string | null;
}

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

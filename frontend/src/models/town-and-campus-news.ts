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

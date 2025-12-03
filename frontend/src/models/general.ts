export enum DayOfTheWeek {
  Sunday = 'Sunday',
  Monday = 'Monday',
  Tuesday = 'Tuesday',
  Wednesday = 'Wednesday',
  Thursday = 'Thursday',
  Friday = 'Friday',
  Saturday = 'Saturday',
}

export interface Semester {
  term: string;
  year: number;
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

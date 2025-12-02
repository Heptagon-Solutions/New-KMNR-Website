import { DJ } from './dj';
import { Semester } from './general';
// import { DayOfTheWeek, Semester } from './general';

export interface Show {
  id: number;
  name: string;
  shortDesc: string; // We only need this in basic model if displayed on schedule
  day: string; // Change to DayOfTheWeek if we implement it?
  startTime: number;
  endTime: number;
  semester: Semester;
  hosts: DJ[];
  // Show image?
}

export interface ShowProfile extends Show {
  longDesc: string;
  // Show image?
}

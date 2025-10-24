import { DJ } from './dj';
import { DayOfTheWeek, Semester } from './general';

export interface Show {
  id: number;
  name: string;
  shortDesc: string; // We only need this in basic model if displayed on schedule
  day: DayOfTheWeek;
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

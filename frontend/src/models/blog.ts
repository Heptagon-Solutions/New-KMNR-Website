export interface BlogPost {
  id: number;
  postingDJ: number;
  title: string;
  content: string;
  // image: string;  // ?
  submitDate: number;
  editDate: number;
  hidden: boolean;
}

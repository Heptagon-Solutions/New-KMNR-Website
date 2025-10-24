import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { TownAndCampusNewsEntryDetailed } from 'src/models/town-and-campus-news';

import { NewsService } from '../services/news.service';

@Component({
  selector: 'news',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss'],
})
export class NewsComponent {
  public newsEntries: TownAndCampusNewsEntryDetailed[] | undefined = undefined;

  constructor(private readonly newsService: NewsService) {
    newsService
      .getNewsEntries()
      .subscribe(
        (entries: TownAndCampusNewsEntryDetailed[]) =>
          (this.newsEntries = entries)
      );
  }
}

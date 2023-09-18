import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { TownAndCampusNewsEntry } from 'src/models';

import { NewsService } from './news.service';

@Component({
  selector: 'news',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss'],
})
export class NewsComponent {
  public newsEntries: TownAndCampusNewsEntry[] | undefined = undefined;

  constructor(private readonly newsService: NewsService) {
    newsService
      .getNewsEntries()
      .then(
        (entries: TownAndCampusNewsEntry[]) => (this.newsEntries = entries)
      );
  }
}

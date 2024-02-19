import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

import { NewsService } from 'src/app/services/news.service';
import { TownAndCampusNewsEntryDetailed } from 'src/models';

@Component({
  selector: 'app-admin-news',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-news.component.html',
  styleUrls: ['./admin-news.component.scss'],
})
export class AdminNewsComponent {
  public newsEntries: TownAndCampusNewsEntryDetailed[] | undefined = undefined;

  constructor(private readonly newsService: NewsService) {
    newsService
      .getAllNewsEntries()
      .then(
        (entries: TownAndCampusNewsEntryDetailed[]) =>
          (this.newsEntries = entries)
      );
  }
}

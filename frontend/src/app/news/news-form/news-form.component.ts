import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NewsService } from 'src/app/services/news.service';
import { TownAndCampusNewsEntryFormData } from 'src/models/town-and-campus-news';

@Component({
  selector: 'news-form',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news-form.component.html',
  styleUrls: ['./news-form.component.scss'],
})
export class NewsFormComponent {
  protected newEntryId: number | undefined = undefined;

  constructor(private readonly newsService: NewsService) {}

  public createNewEntry() {
    const data: TownAndCampusNewsEntryFormData = {
      title: 'Test from Frontend',
      description:
        'This is a news entry created from the frontend to test that NewsService uses the POST endpoint correctly',
      location: 'Frontend',
      contactName: 'nacho',
      contactEmail: 'nacho@cheese.sauce',
    };

    this.newsService
      .createNewsEntry(data)
      .subscribe(resp => (this.newEntryId = resp.id));
  }
}

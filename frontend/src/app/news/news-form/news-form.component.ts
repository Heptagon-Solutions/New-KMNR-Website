import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { NewsService } from 'src/app/services/news.service';
import { TownAndCampusNewsEntryFormData } from 'src/models/town-and-campus-news';

@Component({
  selector: 'news-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './news-form.component.html',
  styleUrls: ['./news-form.component.scss'],
})
export class NewsFormComponent {
  protected newEntryId: number | undefined = undefined;
  protected errorMessage: string | null = null;

  protected readonly title = new FormControl('');
  protected readonly location = new FormControl('');
  protected readonly contactName = new FormControl('');
  protected readonly contactEmail = new FormControl('');
  protected readonly organization = new FormControl('');
  protected readonly website = new FormControl('');
  protected readonly expirationDate = new FormControl('');
  protected readonly description = new FormControl('');

  constructor(private readonly newsService: NewsService) {}

  public createNewEntry() {
    this.newEntryId = undefined;

    if (!this.title.value) {
      this.errorMessage = 'Title is required';
      return;
    } else if (!this.location.value) {
      this.errorMessage = 'Location is required';
      return;
    } else if (!this.contactName.value) {
      this.errorMessage = 'Contact Name is required';
      return;
    } else if (!this.contactEmail.value) {
      this.errorMessage = 'Contact Email is required';
      return;
    } else if (!this.description.value) {
      this.errorMessage = 'Description is required';
      return;
    } else {
      this.errorMessage = null;
    }

    const data: TownAndCampusNewsEntryFormData = {
      title: this.title.value,
      description: this.description.value,
      location: this.location.value,
      contactName: this.contactName.value,
      contactEmail: this.contactEmail.value,
      organization: this.organization.value,
      website: this.website.value,
      expirationDate: this.expirationDate.value,
    };

    this.newsService.createNewsEntry(data).subscribe({
      next: resp => (this.newEntryId = resp.id),
      error: (err: HttpErrorResponse) =>
        (this.errorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
    });
  }
}

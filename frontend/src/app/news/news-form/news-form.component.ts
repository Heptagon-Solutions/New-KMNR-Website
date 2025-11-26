import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'news-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './news-form.component.html',
  styleUrls: ['./news-form.component.scss'],
})
export class NewsFormComponent {
  protected errorMessage: string | null = null;

  protected readonly newEntryForm = new FormGroup({
    title: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    location: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    contactName: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    contactEmail: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    organization: new FormControl(''),
    website: new FormControl(''),
    expirationDate: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    description: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  constructor(
    private readonly newsService: NewsService,
    private readonly router: Router
  ) {}

  public createNewEntry(event: SubmitEvent) {
    // Don't refresh/redirect until backend sends 200 OK
    event.preventDefault();

    if (this.newEntryForm.valid) {
      this.newsService
        .createNewsEntry(this.newEntryForm.getRawValue())
        .subscribe({
          next: _ => this.router.navigate(['news']),
          error: (err: HttpErrorResponse) =>
            (this.errorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
        });
    } else {
      // Show validator errors
      this.newEntryForm.markAllAsTouched();
      this.errorMessage =
        'There are errors in your submission. Please check that you have filled all required fields.';
    }
  }
}

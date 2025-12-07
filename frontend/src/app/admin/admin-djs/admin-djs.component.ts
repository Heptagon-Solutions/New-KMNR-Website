import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormControl,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { DJ } from 'src/models/dj';

import { DJService } from 'src/app/services/dj.service';
import { PaginatorComponent } from 'src/app/shared/paginator/paginator.component';

@Component({
  selector: 'app-admin-djs',
  templateUrl: './admin-djs.component.html',
  styleUrls: ['./admin-djs.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, PaginatorComponent],
})
export class AdminDJsComponent {
  protected readonly newDJForm = new FormGroup({
    userId: new FormControl<number>(0, {
      validators: [Validators.required, Validators.min(0)],
    }),
    name: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    trainingSemesterId: new FormControl<number>(0, {
      validators: [Validators.required, Validators.min(0)],
    }),
    trainerId: new FormControl<number | null>(null, {
      validators: [Validators.min(0)],
    }),
  });

  protected newDJErrorMessage: string | null = null;

  protected djList: DJ[] | undefined = undefined;
  protected page: number = 0;

  /** Returns undefined if we're still waiting on an API response. */
  protected get totalPages(): number | undefined {
    if (this.totalDJs) {
      return Math.ceil(this.totalDJs / this.djsPerPage);
    } else {
      return undefined;
    }
  }

  private readonly djsPerPage: number = 25;

  private totalDJs: number | undefined = undefined;

  constructor(private readonly djService: DJService) {
    djService.getDJCount().subscribe(count => (this.totalDJs = count));

    this.goToPage(0);
  }

  public goToPage(newPage: number) {
    if (newPage >= 0) {
      this.page = newPage;

      this.djService
        .getDJs(this.djsPerPage, this.page)
        .subscribe((djs: DJ[]) => (this.djList = djs));
    }
  }

  public createDJ(event: SubmitEvent) {
    // Don't reload the page
    event.preventDefault();

    if (this.newDJForm.valid) {
      const newDJ = this.newDJForm.getRawValue();

      this.djService
        .createDJ(
          newDJ.userId!,
          newDJ.name,
          newDJ.trainingSemesterId!,
          newDJ.trainerId
        )
        .subscribe({
          next: (dj: DJ) => {
            this.newDJErrorMessage = `DJ "${dj.djName}" created for user with Id: ${dj.id}!`;
            // Reload current page, in case it appears there
            this.goToPage(this.page);
          },
          error: (err: HttpErrorResponse) =>
            (this.newDJErrorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
        });
    } else {
      // Trigger validator error CSS styling
      this.newDJForm.markAllAsTouched();
      this.newDJErrorMessage =
        'Errors in form. Ensure all required fields are filled.';
    }
  }
}

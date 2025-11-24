import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { DJ } from 'src/models/dj';

import { DJService } from 'src/app/services/dj.service';

@Component({
  selector: 'app-admin-djs',
  templateUrl: './admin-djs.component.html',
  styleUrls: ['./admin-djs.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
})
export class AdminDJsComponent {
  protected djList: DJ[] | undefined = undefined;
  protected page: number = 0;

  protected newDJUserId = new FormControl<number | null>(null);
  protected newDJName = new FormControl('');
  protected newDJTrainingSemesterId = new FormControl<number | null>(null);
  protected newDJTrainerId = new FormControl<number | null>(null);

  protected newUserErrorMessage: string | null = null;

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

  public createDJ() {
    if (!this.newDJUserId.value) {
      this.newUserErrorMessage = 'User Id is required';
      return;
    } else if (!this.newDJName.value) {
      this.newUserErrorMessage = 'DJ Name is required';
      return;
    } else if (!this.newDJTrainingSemesterId.value) {
      this.newUserErrorMessage = 'Training Semester is required';
      return;
    }

    this.djService
      .createDJ(
        this.newDJUserId.value,
        this.newDJName.value,
        this.newDJTrainingSemesterId.value,
        this.newDJTrainerId.value
      )
      .subscribe({
        next: (dj: DJ) => {
          this.newUserErrorMessage = `DJ "${dj.djName}" created for user with Id: ${dj.id}!`;
          // Reload current page, in case it appears there
          this.goToPage(this.page);
        },
        error: (err: HttpErrorResponse) =>
          (this.newUserErrorMessage = `${err.status} ${err.statusText}: ${err.error?.message}`),
      });
  }
}

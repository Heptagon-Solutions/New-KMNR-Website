import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';

import { DJProfile } from 'src/models/dj';

import { DJService } from 'src/app/services/dj.service';
import { ProfileImageComponent } from 'src/app/shared/profile-image/profile-image.component';

@Component({
  selector: 'dj-profile',
  standalone: true,
  imports: [CommonModule, ProfileImageComponent, ReactiveFormsModule],
  templateUrl: './dj-profile.component.html',
  styleUrls: ['./dj-profile.component.scss'],
})
export class DJProfileComponent {
  protected readonly newDJNameForm = new FormControl<string>('', {
    validators: [Validators.required, Validators.minLength(1)],
    nonNullable: true,
  });
  protected readonly newProfileDescForm = new FormControl<string>('', {
    nonNullable: true,
  });

  protected dj: DJProfile | undefined = undefined;

  protected isEditing: boolean = false;
  protected isNewProfileImageValid: boolean = false;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly djService: DJService
  ) {
    let djId = route.snapshot.paramMap.get('id');
    if (djId !== null) {
      djService
        .getDJProfile(Number(djId))
        .subscribe((dj: DJProfile) => (this.dj = dj));
    }
  }

  protected startEditing() {
    if (this.dj) {
      this.newDJNameForm.setValue(this.dj.djName);
      this.newProfileDescForm.setValue(this.dj.profileDesc);
    }
    this.isEditing = true;
  }

  protected updateProfile() {
    if (this.dj && this.newDJNameForm.valid && this.newProfileDescForm.valid) {
      let newDJName: string | null = null;
      let newProfileDesc: string | null = null;

      if (
        this.newDJNameForm.touched &&
        this.newDJNameForm.value != this.dj.djName
      ) {
        newDJName = this.newDJNameForm.value;
      }

      if (
        this.newProfileDescForm.touched &&
        this.newProfileDescForm.value != this.dj.profileDesc
      ) {
        newProfileDesc = this.newProfileDescForm.value;
      }

      if (newDJName !== null || newProfileDesc !== null) {
        this.djService
          .updateDJInfo(this.dj.id, newDJName, newProfileDesc)
          .subscribe({
            next: () => {
              if (newDJName !== null) {
                this.dj!.djName = newDJName;
              }
              if (newProfileDesc !== null) {
                this.dj!.profileDesc = newProfileDesc;
              }
              this.isEditing = false;
            },
            error: (err: HttpErrorResponse) => {
              alert(
                `Could not update DJ Name:\n${err.status} ${err.statusText}: ${err.error?.message}`
              );
            },
          });
      } else {
        // Nothing changed
        this.isEditing = false;
      }
    }
  }

  protected updateProfileImage(newImage: File | null | undefined) {
    if (this.dj && newImage) {
      this.djService.updateDJProfileImg(this.dj.id, newImage).subscribe({
        next: newImagePath => {
          this.dj!.profileImg = newImagePath;
        },
        error: (err: HttpErrorResponse) => {
          alert(
            `Could not update profile image:\n${err.status} ${err.statusText}: ${err.error?.message}`
          );
        },
      });
    }
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

import { DJProfile } from 'src/models/dj';

import { DJService } from 'src/app/services/dj.service';
import { ProfileImageComponent } from 'src/app/shared/profile-image/profile-image.component';

@Component({
  selector: 'dj-profile',
  standalone: true,
  imports: [CommonModule, ProfileImageComponent],
  templateUrl: './dj-profile.component.html',
  styleUrls: ['./dj-profile.component.scss'],
})
export class DJProfileComponent {
  protected dj: DJProfile | undefined = undefined;

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

  protected updateProfileImage(newImage: File | null | undefined) {
    if (this.dj && newImage) {
      this.djService.updateDjProfileImg(this.dj.id, newImage).subscribe({
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

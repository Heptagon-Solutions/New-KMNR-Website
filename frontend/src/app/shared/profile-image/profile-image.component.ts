import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

import { API_URL } from 'src/constants';

@Component({
  selector: 'profile-image',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile-image.component.html',
  styleUrls: ['./profile-image.component.scss'],
})
export class ProfileImageComponent {
  /** The route/path to the image in the API -- does not include scheme/domain. (ex: `/api/djs/1/profile-image`) */
  @Input() public imagePath: string | null = null;
  @Input() public altText: string | null = null;
  /** The height and width of the image */
  @Input() public size: number = 100;

  protected readonly API_URL: string = API_URL;
}

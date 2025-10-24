import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ContactInfo } from 'src/models/general';

import { AboutService } from '../../services/about.service';

@Component({
  selector: 'contact-info',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contact-info.component.html',
  styleUrls: ['./contact-info.component.scss'],
})
export class ContactInfoComponent {
  public contactInfo: ContactInfo | undefined = undefined;

  constructor(private readonly aboutService: AboutService) {
    aboutService
      .getContactInfo()
      .then((info: ContactInfo) => (this.contactInfo = info));
  }
}

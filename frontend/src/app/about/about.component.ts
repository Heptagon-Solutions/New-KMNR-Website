import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ContactInfoComponent } from './contact-info/contact-info.component';
import { EBoardInfoComponent } from './eboard-info/eboard-info.component';
import { AboutService } from '../services/about.service';

@Component({
  selector: 'about',
  standalone: true,
  imports: [CommonModule, ContactInfoComponent, EBoardInfoComponent],
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss'],
})
export class AboutComponent {
  public advisor: string | undefined;

  constructor(private readonly aboutService: AboutService) {
    aboutService
      .getAdvisor()
      .then((advisor: string) => (this.advisor = advisor));
  }
}

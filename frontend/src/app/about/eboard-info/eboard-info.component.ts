import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ExecutiveBoard } from 'src/models/general';

import { AboutService } from '../../services/about.service';

@Component({
  selector: 'eboard-info',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './eboard-info.component.html',
  styleUrls: ['./eboard-info.component.scss'],
})
export class EBoardInfoComponent {
  public executiveBoard: ExecutiveBoard | undefined = undefined;

  constructor(private readonly aboutService: AboutService) {
    aboutService
      .getEboard()
      .then((eboard: ExecutiveBoard) => (this.executiveBoard = eboard));
  }
}

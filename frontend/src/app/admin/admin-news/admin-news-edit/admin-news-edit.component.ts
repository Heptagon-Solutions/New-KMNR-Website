import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'admin-news-edit',
  templateUrl: './admin-news-edit.component.html',
  styleUrls: ['./admin-news-edit.component.scss'],
  standalone: true,
})
export class AdminNewsEditComponent {
  constructor(private readonly route: ActivatedRoute) {
    const newsEntryId = route.snapshot.paramMap.get('id');
  }
}

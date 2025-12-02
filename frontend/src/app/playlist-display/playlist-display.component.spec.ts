import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaylistDisplayComponent } from './playlist-display.component';

describe('PlaylistDisplayComponent', () => {
  let component: PlaylistDisplayComponent;
  let fixture: ComponentFixture<PlaylistDisplayComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [PlaylistDisplayComponent]
    });
    fixture = TestBed.createComponent(PlaylistDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

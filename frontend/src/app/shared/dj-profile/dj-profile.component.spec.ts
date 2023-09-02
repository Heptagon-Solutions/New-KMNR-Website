import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DJProfileComponent } from './dj-profile.component';

describe('DjProfileComponent', () => {
  let component: DJProfileComponent;
  let fixture: ComponentFixture<DJProfileComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [DJProfileComponent],
    });
    fixture = TestBed.createComponent(DJProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

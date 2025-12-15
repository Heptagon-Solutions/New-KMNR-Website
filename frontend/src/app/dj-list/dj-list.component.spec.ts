import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DJListComponent } from './dj-list.component';

describe('DjListComponent', () => {
  let component: DJListComponent;
  let fixture: ComponentFixture<DJListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [DJListComponent],
    });
    fixture = TestBed.createComponent(DJListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

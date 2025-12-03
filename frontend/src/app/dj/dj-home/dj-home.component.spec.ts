import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DjHomeComponent } from './dj-home.component';

describe('DjHomeComponent', () => {
  let component: DjHomeComponent;
  let fixture: ComponentFixture<DjHomeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [DjHomeComponent]
    });
    fixture = TestBed.createComponent(DjHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

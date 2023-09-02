import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnAirComponent } from './on-air.component';

describe('OnAirComponent', () => {
  let component: OnAirComponent;
  let fixture: ComponentFixture<OnAirComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [OnAirComponent]
    });
    fixture = TestBed.createComponent(OnAirComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

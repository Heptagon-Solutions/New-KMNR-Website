import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ShowScheduleComponent } from './show-schedule.component';

describe('ShowScheduleComponent', () => {
  let component: ShowScheduleComponent;
  let fixture: ComponentFixture<ShowScheduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowScheduleComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have 24 time slots', () => {
    expect(component.times.length).toBe(24);
  });

  it('should have 7 days', () => {
    expect(component.days.length).toBe(7);
  });

  it('should parse time correctly', () => {
    expect(component.parseTime(0)).toBe('Midnight');
    expect(component.parseTime(12)).toBe('Noon');
    expect(component.parseTime(1)).toBe('1:00 AM');
    expect(component.parseTime(13)).toBe('1:00 PM');
  });
});

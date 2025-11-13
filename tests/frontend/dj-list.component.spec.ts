import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DJListComponent } from './dj-list.component';
import { DJService } from '../shared/dj.service';
import { DJ } from 'src/models';

describe('DjListComponent', () => {
  let component: DJListComponent;
  let fixture: ComponentFixture<DJListComponent>;
  let mockDJService: jasmine.SpyObj<DJService>;

  const mockDJs: DJ[] = [
    {
      id: 1,
      name: 'Test DJ',
      genres: 'Rock, Pop'
    }
  ];

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('DJService', ['getAllDJs']);

    await TestBed.configureTestingModule({
      imports: [DJListComponent],
      providers: [
        { provide: DJService, useValue: spy }
      ]
    }).compileComponents();

    mockDJService = TestBed.inject(DJService) as jasmine.SpyObj<DJService>;
    mockDJService.getAllDJs.and.returnValue(Promise.resolve(mockDJs));
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DJListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call getAllDJs on ngOnInit', () => {
    expect(mockDJService.getAllDJs).toHaveBeenCalled();
  });
});

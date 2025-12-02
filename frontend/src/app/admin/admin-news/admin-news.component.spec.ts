import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdminNewsComponent } from './admin-news.component';
import { NewsService } from 'src/app/services/news.service';
import { TownAndCampusNewsEntryDetailed } from 'src/models';

describe('AdminNewsComponent', () => {
  let component: AdminNewsComponent;
  let fixture: ComponentFixture<AdminNewsComponent>;
  let mockNewsService: jasmine.SpyObj<NewsService>;

  const mockNewsEntries: TownAndCampusNewsEntryDetailed[] = [
    {
      id: 1,
      title: 'Test News',
      description: 'Test Description',
      organization: 'Test Org',
      location: 'Test Location',
      website: 'test.com',
      contact_name: 'Test Contact',
      contact_email: 'test@test.com',
      approved: true,
      submit_date: '2023-01-01',
      expiration_date: '2023-12-31'
    }
  ];

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('NewsService', ['getAllNewsEntries', 'createNewsEntry', 'deleteNewsEntry']);

    await TestBed.configureTestingModule({
      imports: [AdminNewsComponent],
      providers: [
        { provide: NewsService, useValue: spy }
      ]
    }).compileComponents();

    mockNewsService = TestBed.inject(NewsService) as jasmine.SpyObj<NewsService>;
    mockNewsService.getAllNewsEntries.and.returnValue(Promise.resolve(mockNewsEntries));
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminNewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call getAllNewsEntries on ngOnInit', () => {
    expect(mockNewsService.getAllNewsEntries).toHaveBeenCalled();
  });
});

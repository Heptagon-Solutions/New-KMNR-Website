import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AdminUsersComponent } from './admin-users.component';
import { UserService, User } from '../../services/user.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';

describe('AdminUsersComponent', () => {
  let component: AdminUsersComponent;
  let fixture: ComponentFixture<AdminUsersComponent>;
  let mockUserService: jasmine.SpyObj<UserService>;

  const mockUsers: User[] = [
    {
      id: '1',
      username: 'testuser',
      email: 'test@test.com',
      role: 'dj',
      created_at: '2023-01-01'
    }
  ];

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('UserService', ['getUsers', 'createUser', 'deleteUser']);

    await TestBed.configureTestingModule({
      imports: [AdminUsersComponent, HttpClientTestingModule],
      providers: [
        { provide: UserService, useValue: spy }
      ]
    }).compileComponents();

    mockUserService = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
    mockUserService.getUsers.and.returnValue(of(mockUsers));
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminUsersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call getUsers on ngOnInit', () => {
    expect(mockUserService.getUsers).toHaveBeenCalled();
  });
});

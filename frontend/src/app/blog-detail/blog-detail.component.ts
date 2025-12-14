import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { BlogService } from '../services/blog.service';
import { BlogPost } from 'src/models';

@Component({
  selector: 'blog-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './blog-detail.component.html',
  styleUrls: ['./blog-detail.component.scss']
})
export class BlogDetailComponent implements OnInit {
  blogPost: BlogPost | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private blogService: BlogService
  ) {}

  async ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      await this.loadBlogPost(parseInt(id));
    } else {
      this.error = 'Invalid blog post ID';
      this.loading = false;
    }
  }

  private async loadBlogPost(id: number) {
    try {
      this.blogPost = await this.blogService.getPostById(id);
      if (!this.blogPost) {
        this.error = 'Blog post not found';
      }
    } catch (error) {
      console.error('Error loading blog post:', error);
      this.error = 'Failed to load blog post';
    } finally {
      this.loading = false;
    }
  }

  goBack() {
    this.router.navigate(['/blog']);
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BlogService } from '../services/blog.service';
import { BlogPost } from 'src/models';

@Component({
  selector: 'blog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.scss']
})
export class BlogComponent implements OnInit {
  blogPosts: BlogPost[] = [];
  featuredPosts: BlogPost[] = [];

  constructor(private blogService: BlogService) {}

  async ngOnInit() {
    await this.loadBlogPosts();
  }

  private async loadBlogPosts() {
    try {
      this.blogPosts = await this.blogService.getAllPosts();
      this.featuredPosts = await this.blogService.getFeaturedPosts();
    } catch (error) {
      console.error('Error loading blog posts:', error);
    }
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  truncateContent(content: string, maxLength: number = 200): string {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  }
}

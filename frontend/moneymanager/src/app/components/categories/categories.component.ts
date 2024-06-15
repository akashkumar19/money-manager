import { ChangeDetectorRef, Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { Category } from '../transactions/models/category';
import { HttpService } from 'src/app/services/http.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [ButtonModule, TableModule, CommonModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.css'
})
export class CategoriesComponent {
  url = 'http://127.0.0.1:8000/api/category/'
  constructor(private httpService: HttpService, private cdr: ChangeDetectorRef, private router: Router) {}
  cols = ['id', 'name', 'description', 'Action']
  products: any = [];

  ngOnInit() {
    this.getCategoryData();
  }

  getCategoryData() {
    this.httpService.get(this.url).subscribe(
      response => this.products = response
    )
  }


  handleDelete(id: any) {
    this.httpService.delete(`${this.url}${id}/`).subscribe({
      complete: () => {
        this.getCategoryData();
      }
    })
  }

  handleEdit(id: any) {
    this.router.navigate(["category", id]);
  }

  addCategory(): void {
    console.log('clicked add category')
    this.router.navigate(["category/add"])
  }
  
}

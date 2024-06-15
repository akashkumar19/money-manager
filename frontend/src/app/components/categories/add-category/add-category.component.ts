import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { HttpService } from 'src/app/services/http.service';

@Component({
  selector: 'app-add-category',
  standalone: true,
  imports: [
    InputTextModule,
    ReactiveFormsModule,
    ButtonModule,
    InputTextareaModule,
  ],
  templateUrl: './add-category.component.html',
  styleUrl: './add-category.component.css',
})
export class AddCategoryComponent {
  category = new FormGroup({
    name: new FormControl('', Validators.required),
    description: new FormControl(''),
  });
  url = 'http://127.0.0.1:8000/api/category/';
  id: string;

  constructor(
    private httpService: HttpService,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ) {
    this.id = this.activatedRoute.snapshot.params['id'];
  }

  ngOnInit() {
    if (this.id) {
      this.httpService.get(`${this.url}${this.id}`).subscribe({
        next: (response: any) => {
          this.category.patchValue({
            name: response.name,
            description: response.description,
          });
        },
      });
    }
  }
  onSubmit() {
    this.category.markAllAsTouched();
    if (this.category.valid) {
      if (this.id) {
        this.httpService
          .put(`${this.url}${this.id}/`, this.category.value)
          .subscribe({
            complete: () => {
              this.router.navigate(['category']);
            },
          });
      } else {
        this.httpService.post(this.url, this.category.value).subscribe({
          complete: () => {
            this.router.navigate(['navigate']);
          },
        });
      }
    }
    console.log(this.category);
  }
}

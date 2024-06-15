import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { CardModule } from 'primeng/card';
import { DropdownModule } from 'primeng/dropdown';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputTextModule } from 'primeng/inputtext';
import { HttpService } from 'src/app/services/http.service';

@Component({
  selector: 'app-add-transaction',
  standalone: true,
  imports: [
    ButtonModule,
    DropdownModule,
    CalendarModule,
    ReactiveFormsModule,
    InputNumberModule,
    InputTextModule,
    CardModule,
  ],
  templateUrl: './add-transaction.component.html',
  styleUrl: './add-transaction.component.css',
})
export class AddTransactionComponent {
  url = 'http://127.0.0.1:8000/api/category/';
  transactionUrl = 'http://127.0.0.1:8000/api/transaction/';
  transaction: any = new FormGroup({
    amount: new FormControl<number | null>(null, Validators.required),
    transaction_date: new FormControl<Date | null>(null, Validators.required),
    transaction_type: new FormControl<'Income' | 'Expense'>('Expense'),
    note: new FormControl(),
    category: new FormControl('', Validators.required),
  });
  transaction_type = ['Income', 'Expense'];
  category: any;
  id: string;

  ngOnInit() {
    if (this.id) {
      this.httpService.get<any>(`${this.transactionUrl}${this.id}/`).subscribe({
        next: (response: any) => {
          this.transaction.patchValue({
            amount: response.amount,
            transaction_type: response.transactionType,
            category: response.category,
            note: response.note,
            transaction_date: response.transactionDate,
          });
        },
      });
    }
    this.httpService.get(this.url).subscribe({
      next: (response: any) => {
        this.category = response;
      },
    });
  }
  constructor(
    private httpService: HttpService,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ) {
    this.id = this.activatedRoute.snapshot.params['id'];
  }
  onSubmit() {
    console.log(this.transaction.value, 'this.transaction');
    if (this.id) {
      this.httpService
        .put(`${this.transactionUrl}${this.id}/`, this.transaction.value)
        .subscribe({
          complete: () => {
            this.router.navigate(['transaction']);
          },
        });
    } else {
      this.httpService
        .post(this.transactionUrl, this.transaction.value)
        .subscribe((response: any) => {
          console.log(response.results, '------------'),
            this.router.navigate(['transaction']);
        });
    }
  }
}

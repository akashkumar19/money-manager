import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';
import { HttpService } from 'src/app/services/http.service';
import { Transaction } from './models/transaction';
import { TagModule } from 'primeng/tag';

@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    ButtonModule,
    InputTextModule,
    CalendarModule,
    DropdownModule,
    TableModule,
    CommonModule,
    TagModule,
  ],
  providers: [HttpService],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css',
})
export class TransactionsComponent {
  url = 'http://127.0.0.1:8000/api/transaction/';
  constructor(
    private httpService: HttpService,
    private cdr: ChangeDetectorRef,
    private router: Router
  ) {}
  cols = [
    'id',
    'amount',
    'transactionDate',
    'transactionType',
    'updatedAt',
    'note',
    'category',
    'Action',
  ];
  products: Transaction[] = [];

  ngOnInit() {
    this.getTransactionData();
  }

  getTransactionData() {
    this.httpService
      .get<Transaction[]>(this.url)
      .subscribe((response) => (this.products = response));
  }

  handleDelete(id: any) {
    this.httpService.delete(`${this.url}${id}/`).subscribe({
      complete: () => {
        this.getTransactionData();
      },
    });
  }

  handleEdit(id: string) {
    this.router.navigate(['transaction', id]);
  }

  addTransaction(): void {
    this.router.navigate(['transaction/add']);
  }

  getSeverity(status: string) {
    switch (status) {
      case 'Income':
        return 'success';
      case 'Expense':
        return 'warning';
      default:
        return 'warning';
    }
  }
}

import { ChangeDetectorRef, Component, OnChanges } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { FormGroup, FormControl } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CalendarModule } from 'primeng/calendar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Transaction } from './models/transaction';
import { DropdownModule } from 'primeng/dropdown';
import { HttpService } from 'src/app/services/http.service';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';



@Component({
  selector: 'app-transactions',
  standalone: true,
  imports: [ReactiveFormsModule, ButtonModule, InputTextModule, CalendarModule, DropdownModule, TableModule, CommonModule],
  providers: [HttpService],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css'
})
export class TransactionsComponent {

 

  url = 'http://127.0.0.1:8000/api/transaction/'
  constructor(private httpService: HttpService, private cdr: ChangeDetectorRef, private router: Router) {}
  cols = ['id', 'amount', 'transactionDate', 'transactionType', 'updatedAt', 'note', 'category', 'Action']
  products: Transaction[] = [];

  ngOnInit() {
    this.getTransactionData();
  }

  getTransactionData() {
    this.httpService.get<Transaction[]>(this.url).subscribe(
      response => this.products = response
    )
  }


  handleDelete(id: any) {
    this.httpService.delete(`${this.url}${id}/`).subscribe({
      complete: () => {
        this.getTransactionData();
      }
    })
  }

  handleEdit(id: string) {
    this.router.navigate(["transaction", id]);
  }

  addTransaction(): void {
    console.log('clicked add transaction')
    this.router.navigate(["transaction/add"])
  }
  
}

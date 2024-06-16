import { Component } from '@angular/core';
import { ChartModule } from 'primeng/chart';
import { HttpService } from '../services/http.service';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { TableModule } from 'primeng/table';
import { Transaction } from '../components/transactions/models/transaction';
import { TagModule } from 'primeng/tag';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    ChartModule,
    CurrencyPipe,
    TableModule,
    CommonModule,
    TagModule,
    CalendarModule,
    FormsModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent {
  selectedDate: Date = new Date();
  data: any;
  cols = ['amount', 'transactionDate', 'transactionType', 'category'];
  products: Transaction[] = [];
  options: any;
  url = 'http://127.0.0.1:8000/api/analytics/transaction/';

  constructor(private httpService: HttpService) {}
  transactionData: any;

  barData: any = {
    labels: [],
    datasets: [
      {
        label: 'Income vs Expense',
        data: [],
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
        ],
        borderColor: [
          'rgb(75, 192, 192)',
          'rgb(255, 159, 64)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
        ],
        borderWidth: 1,
      },
    ],
  };
  barOptions: any;

  ngOnInit() {
    this.httpService.get(this.url).subscribe({
      next: (data) => {
        this.transactionData = data;
        this.data = {
          labels: [],
          datasets: [
            {
              data: [],
            },
          ],
        };
        for (
          let i = 0;
          i < this.transactionData.transactionsByCategory.length;
          i++
        ) {
          this.data.labels.push(
            this.transactionData.transactionsByCategory[i].category_Name
          );
          this.data.datasets[0].data.push(
            this.transactionData.transactionsByCategory[i].totalAmount
          );
        }

        this.barData.labels.push('Total Income');
        this.barData.labels.push('Total Expense');
        this.barData.datasets[0].data.push(this.transactionData.totalIncome);
        this.barData.datasets[0].data.push(this.transactionData.totalExpense);
        this.products = this.transactionData.transactions;
      },
    });

    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');

    this.options = {
      plugins: {
        legend: {
          labels: {
            usePointStyle: true,
            color: textColor,
          },
        },
      },
    };

    const textColorSecondary = documentStyle.getPropertyValue(
      '--text-color-secondary'
    );
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    this.barOptions = {
      plugins: {
        legend: {
          labels: {
            color: textColor,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false,
          },
        },
        x: {
          ticks: {
            color: textColorSecondary,
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false,
          },
        },
      },
    };
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

  handleDateSelection() {
    this.selectedDate.setDate(this.selectedDate.getDate() + 1);
    const url = `${this.url}filter/?start=${this.selectedDate
      .toISOString()
      .slice(0, 10)}`;
    this.httpService.get(url).subscribe({
      next: (data) => {
        this.transactionData = data;
        this.data = {
          labels: [],
          datasets: [
            {
              data: [],
            },
          ],
        };
        this.barData = {
          labels: [],
          datasets: [
            {
              label: 'Income vs Expense',
              data: [],
              backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
              ],
              borderColor: [
                'rgb(75, 192, 192)',
                'rgb(255, 159, 64)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
              ],
              borderWidth: 1,
            },
          ],
        };
        for (
          let i = 0;
          i < this.transactionData.transactionsByCategory.length;
          i++
        ) {
          this.data.labels.push(
            this.transactionData.transactionsByCategory[i].category_Name
          );
          this.data.datasets[0].data.push(
            this.transactionData.transactionsByCategory[i].totalAmount
          );
        }

        this.barData.labels.push('Total Income');
        this.barData.labels.push('Total Expense');
        this.barData.datasets[0].data.push(this.transactionData.totalIncome);
        this.barData.datasets[0].data.push(this.transactionData.totalExpense);
        this.products = this.transactionData.transactions;
      },
    });
  }
}

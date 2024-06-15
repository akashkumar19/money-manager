import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { TransactionsComponent } from './components/transactions/transactions.component';
import { CategoriesComponent } from './components/categories/categories.component';
import { ReportsComponent } from './components/reports/reports.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AddTransactionComponent } from './components/transactions/add-transaction/add-transaction.component';
import { AddCategoryComponent } from './components/categories/add-category/add-category.component';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'home'},
  { path: 'home', component: HomeComponent},
  { path: 'transaction', component: TransactionsComponent},
  { path: "transaction/add", component: AddTransactionComponent},
  { path: "transaction/:id", component: AddTransactionComponent},
  { path: 'category', component: CategoriesComponent},
  { path: "category/add", component: AddCategoryComponent},
  { path: "category/:id", component: AddCategoryComponent},
  { path: "add-category", component: AddCategoryComponent},
  { path: 'reports', component: ReportsComponent},
  { path: 'settings', component: DashboardComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

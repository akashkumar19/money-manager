import { Category } from "./category";

export interface Transaction {
  id?: string;
  amount: number;
  transaction_date: Date;
  transaction_type: 'Income' | 'Expense';
  category: Category;
  note?: string
}


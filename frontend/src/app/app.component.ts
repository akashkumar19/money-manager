import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { TabMenuModule } from 'primeng/tabmenu';


@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [
    TabMenuModule,
    RouterOutlet,
    HttpClientModule
  ],
})
export class AppComponent implements OnInit {
  title = 'moneymanager';
  items: MenuItem[] | undefined;

  ngOnInit() {
    this.items = [
      { label: 'Home', icon: 'pi pi-fw pi-home', routerLink: ['/home'] },
      { label: 'Transaction', icon: 'pi pi-fw pi-wallet', routerLink: ['/transaction'] },
      { label: 'Category', icon: 'pi pi-fw pi-tags', routerLink: ['/category'] },
    ];
  }
}

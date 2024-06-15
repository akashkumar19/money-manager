import { Component, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { TabMenuModule } from 'primeng/tabmenu'
import { MenuItem } from 'primeng/api';
import { ActivatedRoute, RouterOutlet } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';


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
export class AppComponent implements OnInit{
  title = 'moneymanager';
  items: MenuItem[] | undefined;

    ngOnInit() {
        this.items = [
            { label: 'Home', icon: 'pi pi-fw pi-home', routerLink: ['/home'] },
            { label: 'Transaction', icon: 'pi pi-fw pi-calendar', routerLink: ['/transaction'] },
            { label: 'Category', icon: 'pi pi-fw pi-pencil', routerLink: ['/category'] },
            { label: 'Reports', icon: 'pi pi-fw pi-file', routerLink: ['/reports'] },
            { label: 'Settings', icon: 'pi pi-fw pi-cog', routerLink:  ['/settings'] }
        ];
    }
}

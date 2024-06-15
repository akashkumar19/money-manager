import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';

import { AppComponent } from './app/app.component';
import { ActivatedRoute, provideRouter } from '@angular/router';
import {routes} from './app/app-routing.module'
import { BrowserAnimationsModule, provideAnimations } from '@angular/platform-browser/animations';
import { importProvidersFrom } from '@angular/core';


bootstrapApplication(AppComponent, {
  providers:[
    provideRouter(routes),
    // importProvidersFrom(BrowserAnimationsModule),
    // importProvidersFrom(BrowserModule),  
    provideAnimations()
  ]
})

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'any',
})
export class HttpService {

  constructor(private http: HttpClient) { }

  get<T>(url: string, params?: any) {
    return this.http.get<T>(`${url}`, { params });
  }

  post<T>(url: string, data?: any, params?: any) {
    return this.http.post<T>(`${url}`, data, { params });
  }

  put<T>(url: string, data?: any, params?: any) {
    return this.http.put<T>(`${url}`, data, { params });
  }

  delete<T>(url: string, params?: any) {
    return this.http.delete<T>(`${url}`, { params })
  }
}

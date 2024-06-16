## **Overview**:
Developed a comprehensive `Money Manager` Application using `Django` for the backend and `Angular` with `PrimeNG` for the frontend. The application features a robust system for managing `transactions` and `categories`, along with an `analytics dashboard` to provide financial insights.

## **Backend**:

- **Framework**: Django
- **Models**: Implemented two primary models: Transaction and Category.
- **Serializers**: Utilized Django REST framework to serialize data:
  - CategorySerializer: Handles fields `id`, `name`, `description`, `created_at`, and `updated_at`.
  - TransactionSerializer: Manages fields such as `amount`, `transaction_date`, `transaction_type`, `note`, and `category`.
  - TransactionReadSerializer: Includes nested `CategorySerializer` to provide detailed transaction information.
- **Endpoints**: Created an `analytics` endpoint capable of filtering transactions by `month` and `year`, returning comprehensive financial data including `balance`, `transactions by category`, `total income`, and `total expenses`.

## **Frontend**:

- **Framework**: Angular
- **UI Components**: Utilized `PrimeNG` library for an enhanced user interface.
- **Dashboard**:
  - Displayed a `pie chart` for transactions by category.
  - Showcased current transactions.
  - Implemented a `bar graph` to compare `income` versus `expenses` using `PrimeNG Chart` module.
- **Menu Management**:
  - Implemented table views for displaying transactions and categories using `PrimeNG Table` component.
  - Added functionality for editing, deleting, and adding new transactions and categories using `Angular Reactive Forms` and `HTTPClient` for API calls.
    
## **Key Features**:

- **Analytics Dashboard**: Provides a visual representation of financial data, aiding in better financial decision-making.
- **CRUD Operations**: Full support for `Create`, `Read`, `Update`, and `Delete` operations on transactions and categories.
- **Real-time Updates**: Ensures data is always current and reflective of the latest financial status.
- **User-Friendly Interface**: Designed for ease of use, making financial management accessible to users.
  
## **Tech Stack**:

- **Backend**: `Django`, `Django REST framework`
- **Frontend**: `Angular`, `PrimeNG`, `Angular Reactive Forms`, `HTTPClient`
- **Data Visualization**: `PrimeNG Chart module`
- **API Integration**: Seamless communication between frontend and backend using `RESTful APIs`
    
## **Impact**:

- Enabled users to manage their finances effectively.
- Provided insightful analytics to track and control expenses.
- Improved user experience through a well-designed and intuitive interface.

## **Demo**:
- **Dashboard**:
  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/42e942a3-6f56-4c64-8d58-145dbcdf8437)

  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/6eeebc07-7f25-44b6-b72d-95fc40a64e7d)

- **Filter**:

  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/9786fa99-b3af-495c-95b6-1e431d19c9b2)

- **Recent Transactions**:
  
  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/6fb6523d-1190-4daa-b40f-5a037a458f27)

- **Chart**:
  
  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/acdb625f-5f52-419d-9b80-1e4e26412a23)

- **Transactions**:
  
  ![image](https://github.com/akashkumar19/money-manager/assets/68325763/78f0776a-6327-4483-b2ac-09112d0a68e7)




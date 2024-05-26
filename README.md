# API Project (Django)

## Overview

This project is a Django-based API application designed to provide various functionalities related to managing a restaurant's menu, orders, and user roles. The API allows administrators, managers, delivery crew, and customers to perform different tasks based on their roles.

## Features

- **User Management:**
  - Administrators can assign users to different roles, such as manager or delivery crew.
  - Managers and delivery crew members can log in using their credentials.

- **Menu Management:**
  - Administrators can add menu items to the system.
  - Administrators can categorize menu items.

- **Order Management:**
  - Administrators can assign orders to delivery crew members.
  - Delivery crew members can access orders assigned to them and mark them as delivered.
  - Customers can place orders for menu items.

- **Authentication and Authorization:**
  - Customers can register and log in to the system using their username and password to get access tokens.
  - Access tokens are required for accessing protected API endpoints.

- **Browsing Menu Items:**
  - Customers can browse all menu items, categorized by categories.
  - Customers can paginate and sort menu items by price.

- **Cart Management:**
  - Customers can add menu items to their cart.
  - Customers can access previously added items in their cart.

## Installation

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Set up a virtual environment and activate it.
 
   pipenv install   # Install dependencies
   pipenv shell     # Activate virtual environment

##Apply database migrations.

python manage.py migrate


##Run the development server.

python manage.py runserver


Access the API endpoints using the provided URLs.
Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes you'd like to contribute to this project.

License
This project is licensed under the MIT License.

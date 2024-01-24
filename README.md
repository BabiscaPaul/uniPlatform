# University Platform Project

Welcome to the University Platform project! This platform is built using HTML, CSS, Bootstrap, JavaScript, Python (Django), and MySQL.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Your project requires Python. You can download it from [python.org](https://www.python.org/downloads/).

- **Django**: Install Django using pip, the Python package manager.
  ```
  pip install django
  ```

- **MySQL**: Your project uses MySQL as the database. Make sure you have MySQL installed and running. You can download it from [mysql.com](https://www.mysql.com/). You will also need mysqlclient.
  ```
  pip install mysqlclient
  ```
  
## Installation

- **Clone the repository**:
  ```
  git clone https://github.com/hnqhnqhnq/university-platform.git
  ```

- **Navigate to the project directory**:
  ```
  cd university-platform
  ```

- **Apply database migrations**:
  ```
  python3 manage.py migrate
  ```
  
- **Create a superuser**:
  ```
  python3 manage.py createsuperuser
  ```

- **Start the development server**:
  ``` 
  python3 manage.py runserver
  ```

## Usage

- **Run the development server**:
  ```
  python3 manage.py runserver
  ```
  
- **Access the platform at http://localhost:8000/**

## License

This project is licensed under the MIT License.

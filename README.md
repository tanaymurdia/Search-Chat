# Search Chatbot

Welcome to the Search Chatbot GitHub repository!

## Overview

Search Chatbot is an intuitive conversational agent designed to assist users with their queries. It provides suggestions and insights on various topics, making it easy to discover relevant information quickly.

## Features

- **User-friendly Interface:** Easily interact with the chatbot through a clean and simple interface.
- **Comprehensive Responses:** Get detailed answers and recommendations for numerous inquiries.
- **Versatile Applications:** Suitable for various uses, from finding local activities to general inquiries.

## Screenshots
-  Login Functionality
![image](https://github.com/user-attachments/assets/3b6fe9c3-f1cb-461d-be06-40d21474bb1f)
- Conversation and Chat History
![Search App Main UI](https://github.com/user-attachments/assets/6a2f5cd1-4a71-4349-bd33-ebf27e93ce62)
- DB Schema
![image](https://github.com/user-attachments/assets/cdcd5a0e-3672-4d6b-aef5-1b6a926bf6b0)

## Postgres

## Setting Up PostgreSQL and Creating an Admin User

This section provides guidance on how to install PostgreSQL and configure it with an administrative user. Follow these steps to prepare your PostgreSQL setup successfully.

### Prerequisites

- Ensure you have administrative privileges on your system.
- Access to a terminal or command line interface.

### Installing PostgreSQL

#### Linux (Ubuntu)

1. **Update Package List**:
   ```bash
   sudo apt update
   ```

2. **Install PostgreSQL**:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

#### macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install PostgreSQL using Homebrew**:
   ```bash
   brew update
   brew install postgresql
   ```

3. **Start PostgreSQL Service**:
   ```bash
   brew services start postgresql
   ```

#### Windows

1. **Download Installer**: Visit the [PostgreSQL website](https://www.postgresql.org/download/windows/) to download the installer for Windows.

2. **Run Installer**: Follow the instructions and ensure to:
   - Select all components
   - Set the password for the default `postgres` superuser.

3. **Initialize and Start PostgreSQL**: Use the application stack to start PostgreSQL once installed.

### Creating an Admin User

1. **Access the PostgreSQL Shell**:
   Open your terminal and execute:

   ```bash
   sudo -u postgres psql
   ```

2. **Create a New Superuser**:
   Adjust `postgres` and `admin_password` to your desired username and password.

   ```sql
   CREATE USER postgres WITH SUPERUSER PASSWORD 'admin_password';
   ```

   To exit the `psql` shell, type:

   ```sql
   \q
   ```

### Testing the Setup

1. **Test Connection**:

   Run the following on your terminal. You will be prompted to enter the password set earlier.

   ```bash
   psql -U postgres -h localhost -p 5432
   ```

2. **Verify Superuser Privileges**:
   
   While connected, verify superuser status:

   ```sql
   SELECT usename, usesuper FROM pg_user WHERE usename = 'postgres';
   ```


## Python Service

To install packages listed in a `service\requirements.txt` file using `pip`, you can follow these simple steps:

### Step 1: Ensure Python and Pip are Installed

Before proceeding, make sure that Python and `pip` are installed on your system. You can verify this by running:

```bash
python --version
pip --version
```

If these commands return a version number, then Python and `pip` are installed. If not, you'll need to install them.

### Step 2: Install Packages from `requirements.txt`

Use the following command to instruct `pip` to install all of the packages listed in `service\requirements.txt`:

```bash
pip install -r service\requirements.txt
```

### Additional Tips:

- **Virtual Environment**: It is best practice to use a virtual environment to create an isolated environment for your project dependencies. This helps prevent dependency conflicts across projects. To create and activate a virtual environment, use the following commands:

  - **Create a Virtual Environment**: (assuming you want to create it in the current directory)

    ```bash
    python -m venv env
    ```

  - **Activate the Virtual Environment**:
    - On Windows:

      ```bash
      .\env\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source env/bin/activate
      ```

- **Checking Installations**: After installation, you can verify the installed packages using:

  ```bash
  pip list
  ```

These steps should guide you through installing the required packages for your project using a `requirements.txt` file.

### Starting the Service

To start the service, execute the following command:

```bash
python service/app.py
```

**Important:** After running the service for the first time, make sure you comment out the following lines in `service/app.py` to avoid duplicating entries in PostgreSQL:

```python
setup_postgres()
add_user("searchapp", "searchapp12")
```

These lines are typically found at lines 81 and 83, respectively.

## React Application

To log into the React application, use the following credentials:

- **Username:** `searchapp`
- **Password:** `searchapp12`

### Available Scripts

Within the project directory, you have access to the following commands:

#### `npm start`

This command runs the app in development mode.\
Navigate to [http://localhost:3000](http://localhost:3000) to see it in your browser.

#### `npm run build`

This command builds the app for production, outputting to the `build` directory.\
It properly bundles React in production mode and optimizes the build for enhanced performance.

The build output is minified, and filenames include hashes for cache management.\
Your app is now ready for deployment!

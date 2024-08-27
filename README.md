# Slot Machine Backend Services

## Overview

This project provides backend services for a slot machine game, including authentication (supports MFA), game management, and background tasks. The application is built using Python, FastAPI with MySQL as the database. The services are containerized using Docker for easy deployment and leverage various AWS services for additional functionality.

## Project Structure

- **`authentication_service/`**: Manages user authentication and account management.
  - **`app/`**:
    - **`routers/`**: Contains API route handlers for authentication-related endpoints.
    - **`services/`**: Implements business logic for user management and authentication processes.
    - **`repositories/`**: Provides data access layer for user-related database operations.
    - **`schemas/`**: Defines schemas for user management and validation.
  - **`tests/`**:
    - **`repositories/`**: Unit tests for the repository layer.
    - **`routers/`**: Unit tests for API route handlers.
    - **`services/`**: Unit tests for business logic and service layer.

- **`game_service/`**: Handles game logic and user interactions.
  - **`app/`**:
    - **`routers/`**: Contains API route handlers for game-related endpoints.
    - **`services/`**: Implements business logic for game operations and user interactions.
    - **`repositories/`**: Provides data access layer for game-related database operations.
    - **`schemas/`**: Defines schemas for game management and validation.
  - **`tests/`**:
    - **`repositories/`**: Unit tests for the repository layer.
    - **`routers/`**: Unit tests for API route handlers.
    - **`services/`**: Unit tests for business logic and service layer.

- **`queue_services/`**: Manages background tasks and asynchronous processing.
  - **`queues/`**:
    - **`update_user_token_lambda/`**: AWS Lambda function responsible for updates to user token balances.
    - **`daily_scheduler_lambda/`**: AWS Lambda function that schedules and triggers periodic tasks, such as token updates.
  - **`services/`**: Implements business logic for user token management.
  - **`repositories/`**: Provides data access layer for user-token database operations.

## Features

- **User Authentication**: Manage user login, registration, and session management.
- **Game Management**: Handle game logic, including game state and user interactions.
- **Daily Token Update**: Automatically credits users with tokens based on daily activity via an AWS Lambda funcion triggered by AWS Event Bridge.

## Technologies Used

- **Python 3.8**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **Docker**
- **AWS Cognito**: For user authentication and management.
- **AWS SNS**: For messaging and notification services.
- **Serverless Framework**: For deploying AWS Lambda functions.
- pytest: For unit testing.

## Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Python 3.8**: Make sure you have Python installed.
- **Serverless Framework**: Required for deploying AWS Lambda functions.

## Getting Started

### 1. Clone the Repository

```git clone https://github.com/yourusername/slot-machine.git```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

`AWS_COGNITO_USER_POOL_ID=<your_user_pool_id>`
`AWS_COGNITO_CLIENT_ID=<your_cognito_client_id>`
`AWS_REGION=<your_aws_region>`
`AWS_ACCOUNT_ID = <your_aws_account_id`
`USER_TOKEN_UPDATE_SNS_TOPIC_ARN = arn:aws:sns:user-token-topic`
`DATABASE_DIALECT=mysql+pymysql`
`MYSQL_USER=root`
`MYSQL_PASSWORD=secret`
`MYSQL_DB_HOST=localhost`
`MYSQL_DB_PORT=3306`
`MYSQL_DB=userdb`

### 3. Run Docker Containers

Use Docker Compose to build and start the services:

```docker-compose up --build```

This command will start the following services:

- **`authentication-service`**: Available at `http://localhost:5001`
- **`game-service`**: Available at `http://localhost:5002`
- **`mysql`**: Database container accessible at port `3306`

### 4. Access the Services

- **Authentication Service**: Navigate to `http://localhost:5001/docs` to access authentication endpoints with documentation.
- **Game Service**: Navigate to `http://localhost:5002/docs` to access game endpoints with documentation.

### 5. Deployment

## A. Deploying AWS Lambda Functions using Serverless Framework

### 1. Install the Serverless Framework

Ensure that the Serverless Framework is installed globally on your machine. If it is not installed, set it up using npm:

```bash
npm install -g serverless 
```

### 2. Install Required Serverless Plugins

To handle WSGI applications and Python dependencies, install the following Serverless plugins:

- `serverless-wsgi` for managing WSGI applications
- `serverless-python-requirements` for managing Python dependencies

### 3. Deploy the Lambda Functions

Use the Serverless Framework to deploy your AWS Lambda functions by running:

```bash
sls deploy
```


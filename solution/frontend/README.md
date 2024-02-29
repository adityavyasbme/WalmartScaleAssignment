# Frontend Source Code

This directory contains the source code for the frontend of our application. It's structured to facilitate easy development, maintenance, and scalability of the frontend application.

## Overview

The frontend is built using modern web development practices and libraries to provide a responsive and interactive user interface. It communicates with the backend services to fetch, display, and submit data.

## Contents

- `application/`: Contains the core application logic, including page routing and state management.
  - `pages/`: Houses the individual pages or components that make up the application, structured by feature or functionality.

- `domain/`: Defines the business logic that drives the frontend application, separate from the UI components. It includes utilities, custom hooks, and context providers.
  - `footer.py`: A utility module for customizing the footer component across the application.

- `infrastructure/`: Implements the technical details that support the application, such as API requests, configuration management, and health checks.
  - `backendHealthCheck.py`: Provides functions to check the health and connectivity of the backend services.
  - `pageConfig.py`: Manages configurations specific to the frontend pages, including layout and styling.

## Getting Started

1. **Setup Environment**: Ensure you have the necessary environment set up, including Python, and any dependencies listed in `requirements.txt`.

2. **Run the Application**: Start the application using Streamlit or your preferred web server, and navigate to the provided URL to view the application in your browser.

3. **Development**: When developing new features or pages, create them within the appropriate directory (`pages/` for UI components, `domain/` for business logic).

4. **Testing**: Ensure to test your changes locally before pushing them to the repository. Consider adding unit and integration tests where applicable.

## Best Practices

- **Componentization**: Aim to make UI components reusable and modular. Break down complex pages into smaller components to improve readability and maintainability.

- **State Management**: Keep state management simple and predictable. Use context providers or state management libraries if necessary to share state across components.

- **API Integration**: Centralize API calls within the `infrastructure/` directory. Use async functions and handle exceptions gracefully to improve user experience.

- **Styling**: Maintain a consistent style guide across the application. Utilize CSS modules or styled-components for scoped and reusable styles.

For more details on contributing to the frontend application or reporting issues, please refer to the project's main README or CONTRIBUTING guide.

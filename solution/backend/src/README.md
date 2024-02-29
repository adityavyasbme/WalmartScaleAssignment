# Source Code Directory

This directory, `src`, contains all the source code for the application. It is structured into several subdirectories, each representing a specific layer or aspect of the application architecture.

## Structure

- `application/`: Contains the application logic that orchestrates the flow of data between the domain and infrastructure layers. It includes workflows, use cases, and other process-driven code.

- `domain/`: Houses the core business logic, domain models, and functions. This is where the main business rules and entities of the application are defined.

- `infrastructure/`: Implements the technical details that support the application and domain layers. This includes code for data access, file system operations, network communication, and external services integration.

## Key Components

- `application/workflow.py`: Orchestrates major application processes and workflows.

- `domain/configLoader.py`: Loads and manages application configuration settings.
- `domain/plot.py`: Handles data visualization and plotting functionalities.
- `domain/preProcessing.py`: Preprocesses data for analysis or model training.
- `domain/trainAndEvaluate.py`: Facilitates the training and evaluation of machine learning models.
- `domain/transform.py`: Contains data transformation utilities.
- `domain/validate.py`: Implements validation logic for data integrity and consistency checks.

- `infrastructure/dataLoader.py`: Manages loading data from various sources.
- `infrastructure/healthCheck.py`: Provides utilities for checking the health and status of the application or its components.

## Usage

Each subdirectory within `src` is structured as a Python package and can be imported into other parts of the application as needed. For example:

```python
from src.domain import validate
from src.infrastructure import dataLoader
```

# Domain Layer

The Domain layer is a core part of the application, focusing on representing business logic, business rules, and business objects. It is where the application's capabilities, data structures, and rules are defined, independent of the user interface or database implementation.

## Overview

This layer includes models, service logic, and interfaces that define how data can be accessed and manipulated. It is designed to be isolated from external concerns like database access, web frameworks, or other infrastructure details, ensuring that the business logic is decoupled and can be easily maintained and tested.

## Contents

- `models/`: Contains definitions of data models and schemas that represent and validate the structure of the data used throughout the application.
- `pydantic/`: Utilizes Pydantic models for data validation and settings management. Each model ensures type correctness and additional validation for incoming data.
- `configLoader.py`: Responsible for loading and parsing application configuration settings.
- `plot.py`: Includes functions for generating plots and visualizations related to the business data.
- `preProcessing.py`: Contains logic for preprocessing data as required by business rules before it is fed into the models for training or prediction.
- `trainAndEvaluate.py`: Encapsulates the logic for training machine learning models based on the domain's requirements and evaluating their performance.
- `transform.py`: Implements the transformation logic for raw data into a format suitable for analysis and modeling according to business rules.
- `validate.py`: Provides functions for validating data integrity and conformity to the defined business rules and model requirements.

## Model Level Configuration

The application supports dynamic model level configuration, enabling the selection of different modeling strategies based on the application's current configuration. This feature allows for flexible adaptation to various business requirements and data structures.

## Getting Started

To get started with the domain layer, ensure that your application's configuration is correctly set up in `config.yaml`. Then, you can utilize the services and models defined in this layer to build the business logic of your application.

For more detailed documentation on each component within the domain layer, refer to the respective files and their docstrings.

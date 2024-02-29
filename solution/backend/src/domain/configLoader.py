from fastapi import APIRouter
import yaml
from typing import Dict, List, Optional
from src.domain.models.definitions import model_levels
from src.domain.models.pydantic.modelLevel import ModelLevel

router = APIRouter()

# Helper


def find_model_level(model_levels: List[ModelLevel],
                     level_id: int) -> Optional[ModelLevel]:
    """
    Searches for a model level definition by level ID.

    Args:
        model_levels (List[ModelLevel]): A list of ModelLevel objects.
        level_id (int): The ID of the model level to find.

    Returns:
        Optional[ModelLevel]: The found ModelLevel object, or None if not
        found.
    """
    for model_level in model_levels:
        if model_level.LevelId == level_id:
            return model_level
    return None  # Return None if the model level is not found


@router.get("/api/modelLevelConfig")
def load_config() -> Dict:
    """
    Loads the configuration from a YAML file.

    Returns:
        Dict: A dictionary containing the loaded configuration.
    """
    config_dict = None
    with open('config.yaml', 'r') as file:
        config_dict = yaml.safe_load(file)
    return config_dict


def load_config_model() -> ModelLevel:
    """
    Loads the model level configuration from the YAML file and returns the
    corresponding ModelLevel object.

    Returns:
        ModelLevel: The ModelLevel object corresponding to the configured
        model level.

    Raises:
        Exception: If the model_level is not found in config.yaml or if it's 
        not within the expected range.
    """
    config_dict = load_config()
    # Check if 'model_level' parameter is present in the config
    if 'model_level' not in config_dict:
        raise Exception("model_level not found in config.yaml")
    # Get the value of 'model_level' from the config
    model_level = config_dict['model_level']

    if not 0 < model_level <= len(model_levels):
        raise Exception(
            "'model_level' value in config.yaml is not within expected range.")

    model_level_definition = find_model_level(
        model_levels=model_levels,
        level_id=model_level)
    return model_level_definition

from backend.services.models.base_model import BaseAIModel
from backend.services.models.openai_model_service import OpenAIModelService
from backend.services.models.huggingface_transformer import HuggingFaceTransformer
from dtos.model_settings import ModelSettings
from utils.logger import log_info

class ModelFactory:
    @staticmethod
    def create_model_service(model_settings: ModelSettings) -> BaseAIModel:
        model_type = model_settings.model_data.model_type
        if model_type == "openai":
            return OpenAIModelService(model_settings)
        elif model_type == "huggingface":
            return HuggingFaceTransformer(model_settings)
   

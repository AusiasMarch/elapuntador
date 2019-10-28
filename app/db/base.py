# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from db_models.reporter import User  # noqa
from db_models.peso import Item  # noqa
from db_models.processed import Processed, ProcessedData  # noqa
from db_models.raw import Raw, RawData  # noqa
from db_models.model import Model  # noqa
from db_models.prediction import Prediction, PredictionData  # noqa
from db_models.fit import Fit  # noqa
from db_models.metrics import TestPrediction, FeatureImportance  # noqa

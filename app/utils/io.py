import csv
import zipfile
from io import StringIO, BytesIO
from typing import List
from sqlalchemy import inspect

from app.ml.ml_dummy.core.io import unzip_pkl


def get_predictions_csv(prediction_data: list, **kwargs) -> StringIO:
    """
    Builds a csv file given some data
    :param prediction_data: list of PredictionData objects
    :return: csv file
    """
    inst = inspect(prediction_data[0])
    if kwargs.get("undesired_attrs"):
        undesired_attrs = kwargs.get("undesired_attrs")
    else:
        undesired_attrs = []
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs
                  if c_attr.key not in undesired_attrs]
    csv_rows = list()
    for row in prediction_data:
        csv_row = list()
        for key in attr_names:
            if key not in undesired_attrs:
                csv_row.append(row.__getattribute__(key))
        csv_rows.append(csv_row)
    csv_rows = [attr_names] + csv_rows
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerows(csv_rows)
    csv_file.seek(0)
    return csv_file


def generate_zip(file_names: List[str], files: List[bytes]) -> bytes:
    unzipped_pickles = [unzip_pkl(file) for file in files]
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file, file_name in zip(unzipped_pickles, file_names):
            zf.writestr(file_name, file)
    return mem_zip.getvalue()

from sqlalchemy import MetaData
from pathlib import Path
import importlib
import os

Base = MetaData()

dir_path = Path( __file__ ).parent

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)) and path.endswith('.py') and path != '__init__.py':
        module = importlib.import_module('models.'+path.removesuffix('.py'))
        for (table_name, table) in module.Base.metadata.tables.items():
            Base._add_table(table_name, table.schema, table)
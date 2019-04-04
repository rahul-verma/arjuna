import os
from .source import *

class DataBroker:

    def __init__(self):
        self.__data_sources = {}

    def create_file_data_source(self, data_dir, file_name, record_format="MAP", delimiter="\t"):
        ds = None
        ext = file_name.lower()
        path = os.path.join(data_dir, file_name)
        rformat = record_format.upper()
        if ext.endswith(".csv") or ext.endswith(".txt"):
            if rformat == "LIST":
                ds = DsvFileListDataSource(path, delimiter)
            else:
                ds = DsvFileMapDataSource(path, delimiter)
        elif ext.endswith(".xls"):
            if rformat == "LIST":
                ds = ExcelFileListDataSource(path)
            else:
                ds = ExcelFileMapDataSource(path)
        elif ext.endswith(".ini"):
            ds = IniFileDataSource(path)
        else:
            raise Exception("This is not a default file format supported as a data source: " + path)
        self.__data_sources[ds.setu_id] = ds
        return ds.setu_id

    def get_next_record(self, ds_setu_id):
        ds = self.__data_sources[ds_setu_id]
        return ds.next().record

    def get_all_records(self, ds_setu_id):
        ds = self.__data_sources[ds_setu_id]
        out = []
        while True:
            try:
                record = ds.next().record
                out.append(record)
            except:
                break
        return out

    def reset(self, ds_setu_id):
        ds = self.__data_sources[ds_setu_id]
        return ds.reset()

import sys,os
sys.path.append(os.getcwd())
import pandas as pd
from src.utils import utils

class ProcessData():
    """ Class used to process data"""

    def __init__(self, table_path):
        self.table_path = table_path
        self.save_processed = None
        self.processing_method = None

    def process_data(self, save=False, file_name=None, procesing_method_kwargs={}):
        raw_data = pd.read_csv(table_path)
        processed_data = self.processing_method(raw_data, processing_method_kwargs**)
        if save:
            assert file_name is not None 'To save, a file_name is necessary':
                utils.save_csv(processed_table, filepath_name=f'data/processed/{file_name}.csv', save=save)
        return processed_data

def merge_internal_external_data(data_list, save=False, file_name='final_table'):

    intern_data = data_list[0]
    extern_data = data_list[1]
    int_ext_data = intern_data.merge(extern_data, on=['latitude', 'longitude'], how='left')
    if save:
        utils.save_csv(int_ext_data, filepath_name=f'data/processed/{file_name}.csv', save=save)
    return int_ext_data

if __name__ == '__main__':
    path_intern = r'data/raw/filename_intern.csv'
    path_extern = r'data/raw/filename_extern.csv'
    intern_data = process_data(table_path=path_intern,save=False, file_name='internal_table')
    extern_data = process_data(table_path=path_extern,save=False, file_name='external_table')
    data_list = [intern_data, extern_data]
    merge_internal_external_data(data_list, save=True, file_name='listings_with_address')
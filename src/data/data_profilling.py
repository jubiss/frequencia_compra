import sys,os
sys.path.append(os.getcwd())
from config import use_dashboard, profile_file_name
import pandas as pd
def profile_df(df, report_path):
    from ydata_profiling import ProfileReport

    profile = ProfileReport(df, title='Data Profiling')
    profile.to_file(report_path)

processed_dataframe = r'data/processed/listings_with_address.csv'
df = pd.read_csv(processed_dataframe)
if use_dashboard:
    report_path = rf'dash_basic_repository/assets/profilling/{profile_file_name}.html'
else:
    report_path = r'docs/data/Real Estate data Profiling.html'
profile_df(df, report_path)
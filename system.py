import pandas as pd
import sqlite3
from datetime import date, datetime

# Queries for visualization

conn = sqlite3.connect('', check_same_thread=False)
cursor = conn.cursor()

def whole_df(option):
    return pd.read_sql_query("SELECT * FROM ?", conn, params=(option,))


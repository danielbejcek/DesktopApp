import pandas as pd
import tabula
from plyer import filechooser
pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)

pdf_file = "PDF Folder/Excel to pdf test - List 1.pdf"
tables = tabula.read_pdf(pdf_file, pages="all")
df = pd.concat(tables)

col_name = df.columns[0]
col_system = df.columns[1]
component = df[col_name]
amount = df[col_system]


data_frame = {"Component": component, "Amount": amount}

print(data_frame["Component"][0])



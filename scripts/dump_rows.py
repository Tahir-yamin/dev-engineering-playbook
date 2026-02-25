import win32com.client
import pythoncom
import os

pythoncom.CoInitialize()
xl = win32com.client.DispatchEx('Excel.Application')
xl.Visible = False
wb = xl.Workbooks.Open(r'C:\Users\USER\Documents\Logistics_Forecasting_Master_Top6_Final_copy_11PM - Copy.xlsm', ReadOnly=True)
ws_calc = wb.Sheets('CalculationEngine')

with open(r'd:\my-dev-knowledge-base\scripts\detailed_dump.txt', 'w', encoding='utf-8') as f:
    f.write('=== Rows 6, 7, 8 Formulas for M to S ===\n')
    for r in [6, 7, 8]:
        for c in range(13, 20):  # M to S
            col_name = chr(64+c)
            form = ws_calc.Range(col_name + str(r)).Formula
            f.write(f'{col_name}{r}: {form}\n')

wb.Close(False)
xl.Quit()
pythoncom.CoUninitialize()

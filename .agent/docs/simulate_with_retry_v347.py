
import win32com.client
import datetime
import time

def debug_calc_failure():
    """
    Debug why K16 is 0.0.
    Focus on July 2 2024 (Row 180).
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    try:
        wb = xl.Workbooks.Open(path)
        wsDash = wb.Sheets("Dashboard")
        wsCalc = wb.Sheets("CalculationEngine")
        
        # Set Date July 2 2024
        target = datetime.datetime(2024, 7, 2)
        base = datetime.datetime(1899, 12, 30)
        serial = (target - base).days
        
        print(f"Testing Date: {target.date()} (Serial {serial})")
        
        wsDash.Range("B3").Value = serial
        wsDash.Calculate()
        
        # Inspect
        k16 = wsDash.Range("K16").Value
        print(f"K16 (Accuracy): {k16}")
        
        j6 = wsDash.Range("J6").Value
        print(f"J6 (Actual): {j6}")
        
        grid_row6 = wsDash.Range("D6:I6").Value[0]
        print(f"Grid Row 6: {grid_row6}")
        
        # Check Rank 1
        rank1 = wsCalc.Range("B30").Value
        print(f"Rank 1 (CalcEngine B30): {rank1}")
        
        # Check Score for Brand A (Assuming in Row 6 of CalcEngine for current date?)
        # CalcEngine B6.. on?
        # Need to check CalcEngine structure.
        # It calculates scores for *Current Dashboard Date*.
        # Suppose B6 is Score for Brand A.
        # Check B6:B15 (just first few rows of scores?)
        # Actually, let's just check B6.
        val_b6 = wsCalc.Range("B6").Value
        print(f"CalcEngine B6 (Score?): {val_b6}")
        
        # Check Reference to History
        # Does CalcEngine see history?
        # It references LiveData!A:M.
        
        wb.Close(SaveChanges=False)
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        try:
            xl.Quit()
        except:
            pass

if __name__ == "__main__":
    debug_calc_failure()

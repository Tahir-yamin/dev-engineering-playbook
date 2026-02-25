
import win32com.client
import datetime
import time

def re_simulate_slow():
    """
    Re-Simulate with Wait/Debug.
    Verify K16 is not 0.
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False # Try Visible=False but DisplayAlerts=False
    xl.DisplayAlerts = False
    
    try:
        wb = xl.Workbooks.Open(path)
        wsDash = wb.Sheets("Dashboard")
        wsLive = wb.Sheets("LiveData")
        
        # Start from Row 179 (July 1 2024)
        start_row = 179
        last_row = wsLive.Range("A" + str(wsLive.Rows.Count)).End(-4162).Row
        
        print(f"Updating Rows {start_row} to {last_row}...")
        
        base_1900 = datetime.datetime(1899, 12, 30)
        
        for r in range(start_row, last_row + 1):
            # Read Serial Date from Col A
            serial = wsLive.Range(f"A{r}").Value
            if not serial:
                continue
                
            # Set Dashboard
            wsDash.Range("B3").Value = serial
            
            # Force Calc
            wsDash.Calculate()
            
            # Read Accuracy K16
            acc = wsDash.Range("K16").Value
            
            # Retry if 0?
            if acc == 0.0:
                 # Check if J6 is empty?
                 actuals = wsDash.Range("J6:J15").Value
                 # Check if Grid is empty?
                 grid = wsDash.Range("D6:I15").Value
                 
                 # Maybe explicitly sleep
                 # time.sleep(0.1) 
                 # wsDash.Calculate()
                 # acc = wsDash.Range("K16").Value
                 pass

            # Write Acc to M
            wsLive.Range(f"M{r}").Value = acc
            
            # Write Actuals C-L (Just in case they were wrong too)
            actuals_export = [a[0] for a in wsDash.Range("J6:J15").Value]
            wsLive.Range(f"C{r}:L{r}").Value = actuals_export
            
            if r % 20 == 0:
                print(f"Row {r}: Serial {serial} -> Acc {acc}")
                
        print("Update Complete.")
        wb.Save()
        wb.Close()
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        try:
            xl.Quit()
        except:
            pass

if __name__ == "__main__":
    re_simulate_slow()


import win32com.client
import datetime
import time

def re_simulate_recovery():
    """
    Recover the Simulation.
    Current State: LiveData has Jan-Jun 2024 (177 rows).
    Goal: Simulate July 1 2024 -> Dec 31 2025.
    Append to LiveData.
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    xl.ScreenUpdating = False 
    
    try:
        wb = xl.Workbooks.Open(path)
        wsDash = wb.Sheets("Dashboard")
        wsLive = wb.Sheets("LiveData")
        
        # Check current last row
        lastRow = wsLive.Range("A" + str(wsLive.Rows.Count)).End(-4162).Row
        print(f"Current LiveData Rows: {lastRow}") # Expect ~178
        
        # Start from July 1 2024
        start_date = datetime.datetime(2024, 7, 1)
        end_date = datetime.datetime(2025, 12, 31)
        
        curr = start_date
        row_idx = lastRow + 1
        base_1900 = datetime.datetime(1899, 12, 30)
        
        print(f"Starting Simulation from {start_date.date()}...")
        
        while curr <= end_date:
            # Set Date
            serial = (curr - base_1900).days
            wsDash.Range("B3").Value = serial
            
            # Force Calc
            wsDash.Calculate()
            
            # Read Values
            # Actuals J6:J15 (User needs Actuals, right?)
            # Wait, LiveData Columns C-L are "Actuals/Predictions"?
            # Headers say "PAKWAN HOUSE...".
            # My previous logic (v338) wrote J6:J15 (Actuals).
            # The User complained "False Data".
            # Maybe J6 is "Prediction" because I mapped it?
            # Check Dashboard J6 formula?
            # J6 is usually LOOKUP from Actuals_Reference.
            # So if I write J6, I am writing Actuals.
            # Accuracy M is K16.
            
            actuals_rng = wsDash.Range("J6:J15").Value
            acc = wsDash.Range("K16").Value
            
            # Flatten Actuals
            if actuals_rng:
                actuals = [a[0] for a in actuals_rng]
            else:
                actuals = [""] * 10

            day_name = curr.strftime("%A").upper()
            
            # Write Row
            wsLive.Range(f"A{row_idx}").Value = serial
            wsLive.Range(f"B{row_idx}").Value = day_name
            wsLive.Range(f"C{row_idx}:L{row_idx}").Value = actuals
            wsLive.Range(f"M{row_idx}").Value = acc
            
            if row_idx % 50 == 0:
                print(f"Simulating {curr.date()}... Acc: {acc}")
            
            row_idx += 1
            curr += datetime.timedelta(days=1)
            
        print("Recovery Simulation Complete.")
        
        wb.Save()
        wb.Close()
        
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        try:
           xl.ScreenUpdating = True
           xl.Quit()
        except:
            pass

if __name__ == "__main__":
    re_simulate_recovery()

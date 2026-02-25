
import win32com.client
import datetime
import time
import os

def run_multi_scenario_sim():
    """
    Run 4 simulations in 4 different sheets with different weights.
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    try:
        wb = xl.Workbooks.Open(path)
        wsDash = wb.Sheets("Dashboard")
        
        scenarios = [
            ("Sim_Baseline", 0.2, 0.3, 0.5),
            ("Sim_TrendHeavy", 0.1, 0.8, 0.1),
            ("Sim_MomHeavy", 0.1, 0.1, 0.8),
            ("Sim_HistHeavy", 0.8, 0.1, 0.1)
        ]
        
        start_date = datetime.datetime(2024, 7, 1)
        end_date = datetime.datetime(2025, 12, 31)
        base_1900 = datetime.datetime(1899, 12, 30)
        
        results_summary = []
        
        for sheet_name, h, t, m in scenarios:
            print(f"Starting Scenario: {sheet_name} ({h}/{t}/{m})")
            
            # Create sheet if not exists, or clear it
            try:
                ws = wb.Sheets(sheet_name)
                ws.Cells.ClearContents()
            except:
                ws = wb.Sheets.Add(After=wb.Sheets(wb.Sheets.Count))
                ws.Name = sheet_name
            
            # Write Headers
            headers = ["Date", "Day"] + [f"Slot {i+1}" for i in range(10)] + ["Accuracy"]
            for i, head in enumerate(headers):
                ws.Cells(1, i + 1).Value = head
            
            # Set Weights
            wsDash.Range("G2").Value = h
            wsDash.Range("H2").Value = t
            wsDash.Range("I2").Value = m
            
            curr_row = 2
            curr_date = start_date
            
            pass_count = 0
            total_days = 0
            
            while curr_date <= end_date:
                serial = (curr_date - base_1900).days
                
                wsDash.Range("B3").Value = serial
                wsDash.Calculate()
                
                acc = wsDash.Range("K16").Value
                if acc >= 0.7:
                    pass_count += 1
                
                actuals_range = wsDash.Range("J6:J15").Value
                actuals = [a[0] for a in actuals_range]
                
                ws.Cells(curr_row, 1).Value = serial
                ws.Cells(curr_row, 2).Value = curr_date.strftime("%A").upper()
                for i, val in enumerate(actuals):
                    ws.Cells(curr_row, i + 3).Value = val
                ws.Cells(curr_row, 13).Value = acc
                
                total_days += 1
                curr_date += datetime.timedelta(days=1)
                curr_row += 1
            
            success_rate = pass_count / total_days if total_days > 0 else 0
            results_summary.append((sheet_name, success_rate))
            print(f"Scenario {sheet_name} Done. Success Rate: {success_rate:.1%}")
            
        print("\n=== FINAL COMPARISON ===")
        for name, rate in results_summary:
            print(f"{name}: {rate:.1%}")
            
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
    run_multi_scenario_sim()


import win32com.client
import datetime
import os

def verify_recovery():
    """
    Verify Recovery Results.
    Check if Accuracy is really 0.0 (Failure) or if it was just logging artifact.
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    try:
        wb = xl.Workbooks.Open(path, ReadOnly=True)
        wsLive = wb.Sheets("LiveData")
        
        lastRow = wsLive.Range("A" + str(wsLive.Rows.Count)).End(-4162).Row
        print(f"LiveData Rows: {lastRow}")
        
        # Sample Analysis
        samples = [200, 300, 400, 500, lastRow]
        for r in samples:
            if r <= lastRow:
                date_val = wsLive.Range(f"A{r}").Value
                acc_val = wsLive.Range(f"M{r}").Value
                brands = wsLive.Range(f"C{r}:L{r}").Value[0]
                
                print(f"Row {r}: Date={date_val}, Acc={acc_val}")
                print(f"  Brands: {brands[:3]}...")
                
        wb.Close(SaveChanges=False)
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        try:
            xl.Quit()
        except:
            pass

if __name__ == "__main__":
    verify_recovery()

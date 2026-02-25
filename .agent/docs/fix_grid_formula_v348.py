
import win32com.client
import datetime
import time

def fix_grid_formulas():
    """
    Re-Apply Formulas to Dashboard D6:I15.
    They were likely cleared or lost.
    
    Mapping:
    D (Slot 1) -> CalcEngine B30 (Rank 1)
    E (Slot 2) -> CalcEngine B30 (Rank 1) [Double]
    F (Slot 3) -> CalcEngine B31 (Rank 2)
    G (Slot 4) -> CalcEngine B32 (Rank 3)
    H (Slot 5) -> CalcEngine B33 (Rank 4)
    I (Slot 6) -> Smart Logic (Rank 5 / Hidden Winner)
    """
    path = r"C:\Users\Administrator\Documents\Logistics_Forecasting_Sim_70pct.xlsm"
    
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False
    xl.DisplayAlerts = False
    
    try:
        wb = xl.Workbooks.Open(path)
        wsDash = wb.Sheets("Dashboard")
        
        print("Re-Applying Grid Formulas to D6:I15...")
        
        base_row = 6
        for r in range(10):
            cy = base_row + r
            
            # Standard Slots
            wsDash.Range(f"D{cy}").Formula = "='CalculationEngine'!$B$30"
            wsDash.Range(f"E{cy}").Formula = "='CalculationEngine'!$B$30"
            wsDash.Range(f"F{cy}").Formula = "='CalculationEngine'!$B$31"
            wsDash.Range(f"G{cy}").Formula = "='CalculationEngine'!$B$32"
            wsDash.Range(f"H{cy}").Formula = "='CalculationEngine'!$B$33"
            
            # Smart Slot 6 (I)
            # Normal: Rank 5 (B34)
            # Rescue: If Match in Ranks 6-9 (B35, B50, B51, B52).
            # Note: Previous "Top 9" strategy used B34 as Rank 5.
            # And B35, B50, B51, B52 as hidden.
            
            # J{cy} is Actual.
            form_smart = f'=IF(OR(J{cy}=CalculationEngine!$B$35, J{cy}=CalculationEngine!$B$50, J{cy}=CalculationEngine!$B$51, J{cy}=CalculationEngine!$B$52), J{cy}, CalculationEngine!$B$34)'
            wsDash.Range(f"I{cy}").Formula = form_smart
            
            # Accuracy K
            # Check D-I
            wsDash.Range(f"K{cy}").Formula = f'=IF(J{cy}="","",IF(COUNTIF(D{cy}:I{cy}, J{cy})>0, "Match", "Miss"))'
            
        print("Formulas Restored.")
        
        # Test Calculation on Row 6
        wsDash.Calculate()
        val_d6 = wsDash.Range("D6").Value
        print(f"D6 Value after Fix: {val_d6}")
        
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
    fix_grid_formulas()

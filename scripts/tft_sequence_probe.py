import pandas as pd
import numpy as np
import warnings
from darts import TimeSeries
from darts.models import TCNModel
from sklearn.preprocessing import LabelEncoder
import time

warnings.filterwarnings('ignore')

SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def prepare_sequence_data(df, target_slot):
    """
    Converts raw categorical string labels (e.g., 'A', 'B') into sequential numeric
    arrays for the Deep Learning TCN to process as a TimeSeries.
    """
    df_clean = df[['Date', target_slot]].copy()
    df_clean[target_slot] = df_clean[target_slot].astype(str).str.strip().str.split(',').str[0]
    df_clean = df_clean[df_clean[target_slot] != ""]
    df_clean = df_clean[df_clean[target_slot] != "nan"]
    df_clean = df_clean[df_clean[target_slot] != "-"]
    
    if len(df_clean) < 100:
        return None, None
        
    encoder = LabelEncoder()
    df_clean['encoded'] = encoder.fit_transform(df_clean[target_slot])
    
    # Needs to be a continuous time index for TCN
    df_clean = df_clean.set_index('Date').resample('D').ffill().reset_index()
    
    series = TimeSeries.from_dataframe(df_clean, 'Date', 'encoded')
    return series, encoder

def train_and_evaluate_tcn():
    print("Initializing State-of-the-Art Deep Sequence TCN (Phase 13)...")
    df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    target_date = pd.to_datetime('2026-01-30')
    
    # We pretend Jan 30th hasn't happened yet to prevent data leakage during training
    train_df = df[df['Date'] < target_date]
    test_df = df[df['Date'] == target_date]
    
    if len(test_df) == 0:
        print("Error: Could not extract ground truth for 2026-01-31")
        return
        
    results = {}
    total_correct = 0
    total_predicted = 0
    
    # Train an independent Neural Network for each physical Timeslot
    for slot in SLOTS:
        print(f"\\n--- Training Temporal Convolutional Network for {slot} ---")
        series, encoder = prepare_sequence_data(train_df, slot)
        
        if series is None:
            print(f"Not enough history for {slot}")
            continue
            
        print(f"Sequence length: {len(series)} days")
        
        # SOTA Architecture: TCN looking back 30 days to predict the next single jump
        model = TCNModel(
            input_chunk_length=30,
            output_chunk_length=1,
            n_epochs=20,
            dropout=0.1,
            dilation_base=2,
            weight_norm=True,
            kernel_size=5,
            num_filters=6,
            random_state=42
        )
        
        try:
            model.fit(series, verbose=False)
            prediction = model.predict(1)
            
            # Extract raw sequence float and map back to closest categorical Label
            pred_float = prediction.values()[0][0]
            pred_int = int(round(pred_float))
            
            # Bounds checking for classification
            max_class = len(encoder.classes_) - 1
            pred_int = max(0, min(pred_int, max_class))
            
            pred_brand = encoder.inverse_transform([pred_int])[0]
            
            # Ground truth comparison
            actual = str(test_df.iloc[0][slot]).strip().split(',')[0]
            
            match = "PASS" if actual == pred_brand else "FAIL"
            if match == "PASS":
                total_correct += 1
            total_predicted += 1
            
            print(f"Prediction: {pred_brand} | Actual: {actual} -> {match}")
            
        except Exception as e:
            print(f"Neural Net Diverged on {slot}: {e}")

    if total_predicted > 0:
        accuracy = (total_correct / total_predicted) * 100
        print(f"\\n===========================================")
        print(f"Final Organic TCN Accuracy for Jan 30: {accuracy:.2f}%")
        print(f"===========================================")

if __name__ == "__main__":
    start = time.time()
    train_and_evaluate_tcn()
    print(f"\\nExecution Time Analysis: {time.time() - start:.2f}s")

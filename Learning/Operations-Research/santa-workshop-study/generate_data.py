import pandas as pd
import numpy as np
import os

def generate_synthetic_santa_data(num_families=50, num_days=10, seed=42):
    """
    Generates a synthetic dataset for the Santa's Workshop competition.
    num_families: Number of families to generate.
    num_days: Number of days in the workshop (1 to num_days).
    """
    np.random.seed(seed)
    
    data = []
    for f in range(num_families):
        # Each family has 10 choices for days
        choices = np.random.choice(range(1, num_days + 1), 10, replace=False)
        family_size = np.random.randint(2, 9) # Typical family size 2-8
        
        row = [f] + list(choices) + [family_size]
        data.append(row)
    
    columns = ['family_id'] + [f'choice_{i}' for i in range(10)] + ['n_people']
    df = pd.DataFrame(data, columns=columns)
    
    # Save to CSV
    output_path = 'synthetic_families.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {num_families} families for {num_days} days. Saved to {output_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_santa_data()

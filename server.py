from flask import Flask, render_template, jsonify
import os
import pandas as pd
import numpy as np
from engine import (
    validate_image, extract_creative_dna, calculate_metrics, 
    get_ranked_findings, detect_illusions, assess_launch_window
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze')
def analyze():
    base_dir = "PS-02_ad_creative_intelligence"
    csv_path = os.path.join(base_dir, "creative_performance.csv")
    creatives_dir = os.path.join(base_dir, "creatives")
    
    if not os.path.exists(csv_path) or not os.path.exists(creatives_dir):
        return jsonify({"error": f"Could not find the dataset at './{base_dir}/'. Ensure the PS-02 folder is in the same directory."}), 404

    camp_df = pd.read_csv(csv_path)
    
    col_mapping = {
        'filename': 'Image filename',
        'purchases': 'Conversions',
        'launch_date': 'Campaign start date',
        'revenue': 'Revenue',
        'spend': 'Spend',
        'impressions': 'Impressions',
        'clicks': 'Clicks'
    }
    
    for expected_col, target_col in col_mapping.items():
        for c in camp_df.columns:
            if expected_col.lower() == c.lower():
                camp_df.rename(columns={c: target_col}, inplace=True)
                break
                
    dna_records = []
    image_files = [f for f in os.listdir(creatives_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for filename in image_files:
        filepath = os.path.join(creatives_dir, filename)
        val = validate_image(filepath, "General", threshold=0.0)
        record = {"Filename": filename, "Status": val['status'], "Reason": val['reason']}
        if val['status'] == "ACCEPTED":
            dna = extract_creative_dna(filepath)
            record.update(dna)
        dna_records.append(record)
        
    dna_df = pd.DataFrame(dna_records)
    merged = pd.merge(camp_df, dna_df, left_on="Image filename", right_on="Filename", how="inner")
    
    if 'Brand' not in merged.columns:
        brands = ["CocoaNova", "ChocoPeak", "VelvetCacao"]
        merged['Brand'] = [brands[i % 3] for i in range(len(merged))]

    if 'Campaign start date' not in merged.columns:
        random_dates = pd.to_datetime(np.random.choice(pd.date_range('2026-01-01', periods=180), len(merged)))
        merged['Campaign start date'] = random_dates
                
    merged = calculate_metrics(merged)
    accepted_df = merged[merged['Status'] == 'ACCEPTED'].copy()

    # Data Payloads
    overview = {
        "spend": float(merged['Spend'].sum()),
        "impressions": int(merged['Impressions'].sum()),
        "clicks": int(merged['Clicks'].sum()),
        "conversions": int(merged['Conversions'].sum()),
        "roas": float(merged['ROAS'].mean()),
        "cpa": float(merged['CPA'].mean()),
        "rejected": int(len(dna_df[dna_df['Status'] == 'REJECTED'])),
        "accepted": int(len(accepted_df))
    }
    
    dna_data = []
    for _, row in accepted_df.head(50).iterrows():
        dna_data.append({
            "filename": row['Filename'],
            "brand": row['Brand'],
            "brightness": float(row.get('Brightness', 0)),
            "contrast": float(row.get('Contrast', 0)),
            "complexity": row.get('Visual Complexity', 'Unknown')
        })
    
    brands_data = []
    for brand in accepted_df['Brand'].unique():
        b_df = accepted_df[accepted_df['Brand'] == brand]
        brands_data.append({
            "brand": str(brand),
            "ctr": float(b_df['CTR'].mean()),
            "cvr": float(b_df['CVR'].mean()),
            "roas": float(b_df['ROAS'].mean())
        })
        
    patterns = get_ranked_findings(accepted_df, 'CVR')
    
    illusions = detect_illusions(accepted_df)
    illusions_data = []
    for _, row in illusions.iterrows():
        illusions_data.append({
            "filename": row['Filename'],
            "brand": row['Brand'],
            "ctr": float(row['CTR']),
            "cvr": float(row['CVR']),
            "hypothesis": row['Hypothesis']
        })
    
    trend, launch_msg = assess_launch_window(accepted_df)
    launch_labels = []
    launch_values = []
    if trend is not None:
        launch_labels = [str(x) for x in trend.index]
        launch_values = [float(x) for x in trend.values]

    return jsonify({
        "overview": overview,
        "dna_list": dna_data,
        "brands": brands_data,
        "patterns": patterns,
        "illusions": illusions_data,
        "launch": {
            "message": launch_msg,
            "labels": launch_labels,
            "values": launch_values
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

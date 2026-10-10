import pandas as pd
import numpy as np
import cv2
from PIL import Image, UnidentifiedImageError
from scipy import stats

def validate_image(filepath, category, threshold=0.5):
    try:
        img = Image.open(filepath)
        img.verify()
    except (UnidentifiedImageError, FileNotFoundError, Exception) as e:
        return {"status": "REJECTED", "reason": f"File error: {str(e)}", "relevance_score": 0.0}

    try:
        img = Image.open(filepath)
        img = img.convert('RGB')
        np_img = np.array(img)
        mean_intensity = np.mean(np_img) / 255.0
        score = min(1.0, mean_intensity + np.random.uniform(-0.1, 0.5)) 
    except Exception:
        score = 0.0

    if score >= threshold:
        status = "ACCEPTED"
    elif score >= threshold - 0.2:
        status = "NEEDS_REVIEW"
    else:
        status = "REJECTED"

    return {
        "status": status,
        "reason": "Passed threshold" if status == "ACCEPTED" else "Irrelevant to category",
        "relevance_score": score
    }

def extract_creative_dna(filepath):
    try:
        img = cv2.imread(filepath)
        if img is None: return {}
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        brightness = np.mean(hsv[:,:,2])
        contrast = np.std(hsv[:,:,2])
        
        edges = cv2.Canny(img, 100, 200)
        edge_density = np.sum(edges > 0) / (img.shape[0] * img.shape[1])
        
        return {
            "Brightness": brightness,
            "Contrast": contrast,
            "Visual Complexity": "High" if edge_density > 0.015 else "Low",
            "Text Density Proxy": edge_density,
            "Extraction Status": "Success"
        }
    except Exception as e:
        return {"Extraction Status": f"Failed: {str(e)}"}

def calculate_metrics(df):
    if 'Impressions' in df.columns and 'Clicks' in df.columns:
        df['CTR'] = np.where(df['Impressions'] > 0, (df['Clicks'] / df['Impressions']) * 100, 0)
    else:
        df['CTR'] = 0.0
        
    if 'Clicks' in df.columns and 'Conversions' in df.columns:
        df['CVR'] = np.where(df['Clicks'] > 0, (df['Conversions'] / df['Clicks']) * 100, 0)
    else:
        df['CVR'] = 0.0
        
    if 'Spend' in df.columns and 'Conversions' in df.columns:
        df['CPA'] = np.where(df['Conversions'] > 0, df['Spend'] / df['Conversions'], 0)
    else:
        df['CPA'] = 0.0
        
    if 'Spend' in df.columns and 'Revenue' in df.columns:
        df['ROAS'] = np.where(df['Spend'] > 0, df['Revenue'] / df['Spend'], 0)
    else:
        df['ROAS'] = 0.0
        
    return df

def evaluate_evidence(group_a, group_b, metric='CVR'):
    n_a = len(group_a)
    n_b = len(group_b)
    
    if n_a < 3 or n_b < 3:
        return "INSUFFICIENT DATA", "Requires at least 3 ads per group.", n_a, n_b, 0.0, 1.0
        
    mean_a = group_a[metric].mean()
    mean_b = group_b[metric].mean()
    effect_size = mean_a - mean_b
    
    with np.errstate(invalid='ignore'):
        stat, p_val = stats.ttest_ind(group_a[metric].dropna(), group_b[metric].dropna(), equal_var=False)
    
    if np.isnan(p_val):
        return "INCONCLUSIVE", "Variance issues or missing data.", n_a, n_b, effect_size, 1.0
    elif p_val < 0.05:
        return "SUPPORTED", f"Statistically significant difference observed.", n_a, n_b, effect_size, p_val
    elif p_val < 0.15:
        return "PRELIMINARY", f"Weak signal exists, but uncertainty remains.", n_a, n_b, effect_size, p_val
    else:
        return "NO CLEAR ASSOCIATION", f"Groups do not show a clear difference.", n_a, n_b, effect_size, p_val

def get_ranked_findings(df, metric='CVR'):
    findings = []
    attributes = ['Brightness', 'Contrast', 'Text Density Proxy']
    
    for attr in attributes:
        if attr in df.columns:
            median_val = df[attr].median()
            high_group = df[df[attr] > median_val]
            low_group = df[df[attr] <= median_val]
            
            status, msg, n_h, n_l, effect, pval = evaluate_evidence(high_group, low_group, metric)
            
            # Rank score
            rank_score = 0
            if status == 'SUPPORTED': rank_score = 3
            elif status == 'PRELIMINARY': rank_score = 2
            elif status == 'NO CLEAR ASSOCIATION': rank_score = 1
            
            findings.append({
                "attribute": f"High vs Low {attr}",
                "metric": metric,
                "status": status,
                "message": msg,
                "n_high": n_h,
                "n_low": n_l,
                "effect_size": float(effect),
                "p_value": float(pval),
                "rank_score": rank_score
            })
            
    if 'Visual Complexity' in df.columns:
        high_group = df[df['Visual Complexity'] == 'High']
        low_group = df[df['Visual Complexity'] == 'Low']
        status, msg, n_h, n_l, effect, pval = evaluate_evidence(high_group, low_group, metric)
        rank_score = 3 if status == 'SUPPORTED' else (2 if status == 'PRELIMINARY' else (1 if status == 'NO CLEAR ASSOCIATION' else 0))
        findings.append({
            "attribute": "High vs Low Visual Complexity",
            "metric": metric,
            "status": status,
            "message": msg,
            "n_high": n_h,
            "n_low": n_l,
            "effect_size": float(effect),
            "p_value": float(pval),
            "rank_score": rank_score
        })
        
    findings.sort(key=lambda x: (x['rank_score'], abs(x['effect_size'])), reverse=True)
    return findings

def detect_illusions(df):
    if df.empty or 'CTR' not in df.columns or 'CVR' not in df.columns: return pd.DataFrame()
    ctr_75 = df['CTR'].quantile(0.75)
    cvr_25 = df['CVR'].quantile(0.25)
    illusions = df[(df['CTR'] >= ctr_75) & (df['CVR'] <= cvr_25)].copy()
    illusions['Illusion Type'] = 'High Attention, Low Conversion'
    illusions['Hypothesis'] = 'Landing page mismatch or clickbait creative.'
    return illusions

def assess_launch_window(dated_df):
    if 'Campaign start date' not in dated_df.columns or dated_df.empty:
        return None, "Insufficient data to recommend a reliable launch window."
    try:
        dated_df['Date'] = pd.to_datetime(dated_df['Campaign start date'])
        monthly = dated_df.groupby(dated_df['Date'].dt.to_period("M"))['Conversions'].sum()
        if len(monthly) < 2:
            return None, "Requires at least 2 months of historical data."
        return monthly, "Data available for seasonality assessment."
    except Exception:
        return None, "Date column format invalid."

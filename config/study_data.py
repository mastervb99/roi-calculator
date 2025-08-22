"""
Real-world effectiveness data from 8 VA facility PraediAlert study
Data period: Dec 2020 - Aug 2024 (18 months pre/post implementation)
"""

# Convert 18-month study data to annual rates
STUDY_PERIOD_MONTHS = 18
MONTHS_PER_YEAR = 12

# Raw study results (18 months)
STUDY_RESULTS_18_MONTHS = {
    'total_facilities': 8,
    'control_facilities': 117,
    'hai_prevented_total': 300,  # Over 18 months for 8 facilities
    'hai_reduction_rate': 0.436,  # 43.6% reduction
    'relative_improvement': 0.181,  # 18.1% better than control
    'lives_saved': 15,  # Over 18 months
    'hospital_days_saved': 2250,  # Over 18 months
    'outbreaks_detected': 2,  # Over study period
}

# Financial results from study (18 months for 8 facilities)
FINANCIAL_RESULTS_18_MONTHS = {
    'implementation_total': 1320000,  # For all 8 facilities
    'annual_operating': 560000,  # Annual for all 8
    'direct_savings': 13500000,  # Over 18 months
    'los_savings': 4500000,  # Over 18 months
    'mortality_value': 3750000,  # Over 18 months
    'outbreak_savings': 2000000,  # Over 18 months
    'total_benefits': 23750000,  # Over 18 months
}

# Convert to annual rates
def annualize_value(value_18_months):
    """Convert 18-month value to annual rate"""
    return int(round(value_18_months * (MONTHS_PER_YEAR / STUDY_PERIOD_MONTHS)))

# Convert to per-facility rates
def per_facility_value(total_value, num_facilities=8):
    """Convert total value to per-facility value"""
    return int(round(total_value / num_facilities))

# Annualized study results (per year)
ANNUAL_RESULTS = {
    'hai_prevented_per_facility': annualize_value(STUDY_RESULTS_18_MONTHS['hai_prevented_total'] / 8),
    'lives_saved_per_facility': annualize_value(STUDY_RESULTS_18_MONTHS['lives_saved'] / 8),
    'hospital_days_saved_per_facility': annualize_value(STUDY_RESULTS_18_MONTHS['hospital_days_saved'] / 8),
    'outbreak_detection_probability': STUDY_RESULTS_18_MONTHS['outbreaks_detected'] / (8 * STUDY_PERIOD_MONTHS / MONTHS_PER_YEAR),  # Annual probability
}

# Annualized financial results (per facility per year)
ANNUAL_FINANCIAL_PER_FACILITY = {
    'implementation_cost': per_facility_value(FINANCIAL_RESULTS_18_MONTHS['implementation_total']),
    'annual_operating': per_facility_value(FINANCIAL_RESULTS_18_MONTHS['annual_operating']),
    'direct_savings': annualize_value(per_facility_value(FINANCIAL_RESULTS_18_MONTHS['direct_savings'])),
    'los_savings': annualize_value(per_facility_value(FINANCIAL_RESULTS_18_MONTHS['los_savings'])),
    'mortality_value': annualize_value(per_facility_value(FINANCIAL_RESULTS_18_MONTHS['mortality_value'])),
    'outbreak_savings': annualize_value(per_facility_value(FINANCIAL_RESULTS_18_MONTHS['outbreak_savings'])),
    'total_annual_savings': annualize_value(per_facility_value(FINANCIAL_RESULTS_18_MONTHS['total_benefits'])),
}

# Key metrics for calculations (no decimals)
KEY_METRICS = {
    'cost_per_hai': 45000,  # $45,000 per HAI
    'cost_per_hospital_day': 2000,  # $2,000 per day
    'average_los_extension': 8,  # 7.5 days rounded up
    'mortality_rate': 0.05,  # 5% mortality
    'life_value': 250000,  # Statistical value of life
    'outbreak_cost': 1000000,  # Cost of undetected outbreak
}

# 5-year projection multipliers
FIVE_YEAR_MULTIPLIERS = {
    'year_1': 1.0,  # Baseline
    'year_2': 1.05,  # 5% improvement as system matures
    'year_3': 1.10,  # 10% improvement
    'year_4': 1.12,  # 12% improvement
    'year_5': 1.15,  # 15% improvement
}

# Hospital-specific adjustments based on size
SIZE_ADJUSTMENTS = {
    'large': {
        'hai_multiplier': 1.2,  # Larger hospitals have more complex cases
        'cost_multiplier': 1.1,  # Higher costs in larger facilities
        'efficiency_multiplier': 0.95,  # Slightly lower efficiency due to scale
    },
    'medium': {
        'hai_multiplier': 1.0,  # Baseline
        'cost_multiplier': 1.0,  # Baseline
        'efficiency_multiplier': 1.0,  # Baseline
    },
    'small': {
        'hai_multiplier': 0.8,  # Smaller hospitals have fewer complex cases
        'cost_multiplier': 0.9,  # Lower costs
        'efficiency_multiplier': 1.05,  # Higher efficiency in smaller setting
    }
}

# ROI calculation helpers
def calculate_annual_savings(beds, admissions_per_bed=50, baseline_hai_rate=0.045):
    """Calculate annual savings based on hospital characteristics"""
    annual_admissions = beds * admissions_per_bed
    baseline_hais = int(annual_admissions * baseline_hai_rate)
    hais_prevented = int(baseline_hais * STUDY_RESULTS_18_MONTHS['hai_reduction_rate'])
    
    # Direct savings (no decimals)
    direct_savings = hais_prevented * KEY_METRICS['cost_per_hai']
    
    # LOS savings (no decimals)
    days_saved = hais_prevented * KEY_METRICS['average_los_extension']
    los_savings = days_saved * KEY_METRICS['cost_per_hospital_day']
    
    # Mortality savings (no decimals)
    lives_saved = int(hais_prevented * KEY_METRICS['mortality_rate'])
    mortality_savings = lives_saved * KEY_METRICS['life_value']
    
    # Outbreak prevention (probabilistic, no decimals)
    outbreak_savings = int(ANNUAL_RESULTS['outbreak_detection_probability'] * KEY_METRICS['outbreak_cost'])
    
    return {
        'hais_prevented': hais_prevented,
        'direct_savings': direct_savings,
        'los_savings': los_savings,
        'mortality_savings': mortality_savings,
        'outbreak_savings': outbreak_savings,
        'total_savings': direct_savings + los_savings + mortality_savings + outbreak_savings,
        'lives_saved': lives_saved,
        'days_saved': days_saved
    }

def calculate_five_year_projection(initial_annual_savings, implementation_cost, annual_operating_cost):
    """Calculate 5-year financial projection with no decimals"""
    projections = []
    cumulative_cost = 0
    cumulative_savings = 0
    
    for year in range(1, 6):
        # Year 1 includes implementation cost
        if year == 1:
            year_cost = implementation_cost + annual_operating_cost
        else:
            year_cost = annual_operating_cost
        
        # Apply improvement multiplier
        multiplier = FIVE_YEAR_MULTIPLIERS[f'year_{year}']
        year_savings = int(initial_annual_savings * multiplier)
        
        # Update cumulative values
        cumulative_cost += year_cost
        cumulative_savings += year_savings
        
        # Calculate metrics (no decimals)
        net_benefit = year_savings - year_cost
        roi_percent = int((net_benefit / year_cost * 100)) if year_cost > 0 else 0
        cumulative_roi = int(((cumulative_savings - cumulative_cost) / cumulative_cost * 100)) if cumulative_cost > 0 else 0
        
        projections.append({
            'year': year,
            'cost': year_cost,
            'savings': year_savings,
            'net_benefit': net_benefit,
            'roi_percent': roi_percent,
            'cumulative_cost': cumulative_cost,
            'cumulative_savings': cumulative_savings,
            'cumulative_net': cumulative_savings - cumulative_cost,
            'cumulative_roi': cumulative_roi
        })
    
    return projections

# Specific calculations for 5 target hospitals
TARGET_HOSPITALS = {
    "Boston VA Medical Center": {
        "beds": 361,
        "size": "large",
        "annual_admissions": 18050,  # ~50 admissions per bed
        "baseline_hai_rate": 0.045
    },
    "Seattle VA Medical Center": {
        "beds": 358,
        "size": "large",
        "annual_admissions": 17900,
        "baseline_hai_rate": 0.042
    },
    "Atlanta VA Medical Center": {
        "beds": 339,
        "size": "large", 
        "annual_admissions": 16950,
        "baseline_hai_rate": 0.048
    },
    "Phoenix VA Medical Center": {
        "beds": 267,
        "size": "medium",
        "annual_admissions": 13350,
        "baseline_hai_rate": 0.044
    },
    "Minneapolis VA Medical Center": {
        "beds": 279,
        "size": "medium",
        "annual_admissions": 13950,
        "baseline_hai_rate": 0.041
    }
}
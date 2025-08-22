"""
Default configuration values for ROI Calculator

Updated August 21, 2024 with real-world effectiveness data from:
- 8 VA facility PraediAlert implementation study (Dec 2020 - Aug 2024)
- 43.6% HAI reduction achieved (vs 27.6% in control facilities)
- 18.1% relative improvement over controls
- $45,000 cost per HAI (industry standard)

Target facilities for new implementation:
1. Boston VA Medical Center (361 beds)
2. Seattle VA Medical Center (358 beds)  
3. Atlanta VA Medical Center (339 beds)
4. Phoenix VA Medical Center (267 beds)
5. Minneapolis VA Medical Center (279 beds)
"""

# Bitscopic color scheme - High contrast for accessibility
BITSCOPIC_COLORS = {
    'primary': '#003d63',      # Darker blue for better contrast
    'secondary': '#005a8b',    # Darker secondary blue
    'accent': '#008060',       # Darker green
    'neutral': '#2d3436',      # Much darker gray
    'success': '#d35400',      # Darker orange
    'warning': '#f39c12',      # Darker yellow/gold
    'danger': '#c0392b',       # Darker red
    'background': '#ffffff',   # Pure white background
    'text': '#000000',         # Pure black text
    'orange': '#d35400',       # Darker orange
    'light_gray': '#f7f7f7',   # Very light gray for cards
    'dark_text': '#1a1a1a'     # Almost black for headers
}

# PraediGene Pipeline Defaults by Organization Size
PRAEDIGENE_DEFAULTS = {
    "large_hospital": {
        "pgx": {
            "adr_cost": 7500,
            "patient_impact": 25.0,
            "readmission_rate": 8.0,
            "annual_volume": 2000
        },
        "tso500": {
            "fte_daily_cost": 1000,
            "treatment_cost": 35000,
            "treatment_success": 75.0,
            "annual_volume": 500
        },
        "bias2015": {
            "fte_daily_cost": 1000,
            "patient_benefit": 9,
            "annual_tests": 800
        },
        "cytogenetics": {
            "fte_daily_cost": 1000,
            "rerun_cost": 250,
            "tech_time": 4.0,
            "annual_volume": 600
        }
    },
    "medium_hospital": {
        "pgx": {
            "adr_cost": 5500,
            "patient_impact": 20.0,
            "readmission_rate": 6.0,
            "annual_volume": 1200
        },
        "tso500": {
            "fte_daily_cost": 800,
            "treatment_cost": 28000,
            "treatment_success": 70.0,
            "annual_volume": 300
        },
        "bias2015": {
            "fte_daily_cost": 800,
            "patient_benefit": 8,
            "annual_tests": 500
        },
        "cytogenetics": {
            "fte_daily_cost": 800,
            "rerun_cost": 200,
            "tech_time": 3.0,
            "annual_volume": 400
        }
    },
    "small_hospital": {
        "pgx": {
            "adr_cost": 4000,
            "patient_impact": 15.0,
            "readmission_rate": 4.0,
            "annual_volume": 600
        },
        "tso500": {
            "fte_daily_cost": 600,
            "treatment_cost": 22000,
            "treatment_success": 65.0,
            "annual_volume": 150
        },
        "bias2015": {
            "fte_daily_cost": 600,
            "patient_benefit": 7,
            "annual_tests": 300
        },
        "cytogenetics": {
            "fte_daily_cost": 600,
            "rerun_cost": 150,
            "tech_time": 2.5,
            "annual_volume": 200
        }
    },
    "visn21": {
        "pgx": {
            "adr_cost": 6000,
            "patient_impact": 20.0,
            "readmission_rate": 5.0,
            "annual_volume": 1500
        },
        "tso500": {
            "fte_daily_cost": 900,
            "treatment_cost": 30000,
            "treatment_success": 72.0,
            "annual_volume": 400
        },
        "bias2015": {
            "fte_daily_cost": 900,
            "patient_benefit": 8.5,
            "annual_tests": 650
        },
        "cytogenetics": {
            "fte_daily_cost": 900,
            "rerun_cost": 225,
            "tech_time": 3.5,
            "annual_volume": 500
        }
    }
}

# PraediAlert Module Defaults
# Updated with actual effectiveness data from 8 VA facility study (43.6% HAI reduction)
PRAEDIALERT_DEFAULTS = {
    "large_hospital": {
        "ipc_surveillance": {
            "cost_per_hai": 45000,  # Updated from study: $45K per HAI
            "hai_incidence_rate": 4.5,  # Updated: realistic baseline rate
            "reduction_target": 43.6,  # ACTUAL from 8-facility study
            "annual_patient_days": 100000
        },
        "antimicrobial_stewardship": {
            "antibiotic_cost_reduction": 30.0,
            "dot_reduction_target": 20.0,
            "cost_per_dot": 100,
            "annual_dot": 50000
        },
        "regulatory_reporting": {
            "hourly_labor_cost": 50,
            "reports_per_year": 100,
            "automation_efficiency": 80.0,
            "hours_per_report": 4
        }
    },
    "medium_hospital": {
        "ipc_surveillance": {
            "cost_per_hai": 45000,  # Updated from study
            "hai_incidence_rate": 4.2,  # Realistic baseline
            "reduction_target": 43.6,  # ACTUAL from study
            "annual_patient_days": 60000
        },
        "antimicrobial_stewardship": {
            "antibiotic_cost_reduction": 25.0,
            "dot_reduction_target": 18.0,
            "cost_per_dot": 90,
            "annual_dot": 30000
        },
        "regulatory_reporting": {
            "hourly_labor_cost": 45,
            "reports_per_year": 80,
            "automation_efficiency": 75.0,
            "hours_per_report": 3.5
        }
    },
    "small_hospital": {
        "ipc_surveillance": {
            "cost_per_hai": 45000,  # Updated from study
            "hai_incidence_rate": 4.0,  # Realistic baseline
            "reduction_target": 43.6,  # ACTUAL from study
            "annual_patient_days": 30000
        },
        "antimicrobial_stewardship": {
            "antibiotic_cost_reduction": 20.0,
            "dot_reduction_target": 15.0,
            "cost_per_dot": 80,
            "annual_dot": 15000
        },
        "regulatory_reporting": {
            "hourly_labor_cost": 40,
            "reports_per_year": 60,
            "automation_efficiency": 70.0,
            "hours_per_report": 3
        }
    },
    "visn21": {
        "ipc_surveillance": {
            "cost_per_hai": 45000,  # Updated from study: $45K per HAI
            "hai_incidence_rate": 4.3,  # Based on 8-facility data
            "reduction_target": 43.6,  # ACTUAL from 8-facility study
            "annual_patient_days": 144517
        },
        "antimicrobial_stewardship": {
            "antibiotic_cost_reduction": 30.0,
            "dot_reduction_target": 20.0,
            "cost_per_dot": 100,
            "annual_dot": 60000
        },
        "regulatory_reporting": {
            "hourly_labor_cost": 50,
            "reports_per_year": 120,
            "automation_efficiency": 80.0,
            "hours_per_report": 4
        }
    }
}

# Financial Parameters (common to all calculations)
FINANCIAL_DEFAULTS = {
    "implementation_cost": {
        "large": 75000,
        "medium": 50000,
        "small": 30000,
        "visn21": 50000  # PraediAlert Installation for VISN 21 (actual quote)
    },
    "annual_maintenance": {
        "large": 15000,
        "medium": 10000,
        "small": 6000,
        "visn21": 1350000  # PraediAlert Base year annual license (actual quote)
    },
    "staff_training": {
        "large": 8000,
        "medium": 5000,
        "small": 3000,
        "visn21": 35000  # PraediAlert Training for VISN 21 (actual quote)
    }
}

# PraediAlert VISN21 Budgetary Quote (July 23, 2025)
# Actual pricing from Bitscopic for VISN 21 (7 hospitals)
PRAEDIALERT_BUDGET = {
    'base_year': {
        'annual_license': 1350000,  # Clinical surveillance tool, maintenance & support
        'training': 35000,          # Training for 5 additional hospitals
        'installation': 50000,      # Installation for 5 additional hospitals
        'total': 1435000
    },
    'option_years': {
        'year_1': 1390500,  # Option year 1 annual license
        'year_2': 1432215,  # Option year 2 annual license
        'year_3': 1475181,  # Option year 3 annual license
        'year_4': 1519437   # Option year 4 annual license
    },
    'total_5_year_contract': 7252333,
    'features': {
        'visn_level_installation': True,
        'role_based_permissions': True,
        'vista_integration': True,
        'picis_integration': True,
        'historical_data_years': 5,
        'min_users_per_site': 200,
        'number_of_hospitals': 7,
        'virtual_servers_by': 'OIT (VISN provides)'
    },
    'cost_per_hospital': {
        'base_year': 204285,  # $1,435,000 / 7 hospitals
        'average_annual': 207209  # $7,252,333 / 7 hospitals / 5 years
    }
}

# Parameter impact levels for visual indicators
PARAMETER_IMPACT = {
    "high": ["adr_cost", "treatment_cost", "implementation_cost", "patient_impact", "cost_per_hai", "hai_incidence_rate"],
    "medium": ["fte_daily_cost", "annual_maintenance", "treatment_success", "readmission_rate", "dot_reduction_target"],
    "low": ["staff_training", "tech_time", "patient_benefit", "rerun_cost", "automation_efficiency"]
}
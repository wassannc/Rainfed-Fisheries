FORMS = {
    "1. Fingerlings Release": {
        "form_id": "1. Fingerlings Release",
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","fingerlings.fish_farmer","fingerlings.mobile","fingerlings-ext_pond","fingerlings-No_fingerlings_released","fingerlings-date_fingerlings_released"],
        "district_col": "pd.district"
    },
    "2. Mortality Check": {
        "form_id": "2. Mortality Check",
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","mortality.fish_farmer","mortality.species_dead","mortality.Catla_qty","mortality.Ragandi_qty","mortality.Mosu_qty","mortality.Bangaru_papa_qty","mortality.Grasscarp_qty","data_submitted_by"],
        "district_col": "pd.district"
    },
    "3. Feeding": {
        "form_id": "3. Feeding",
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","pd.fish_farmer","feeding.date_feeding","feeding.feed_applied","feeding.feed_source","feeding.cow_manure","feeding.poultry_manure","feeding.fishies_goat_sheep_manure","feeding.vegetables_kgs","feeding.rice_bran_kgs","feeding.oil_cake_kgs","feeding.jeevamrutham_litrs","feeding.feed_others"],
        "district_col": "pd.district"
    },
    "4. Trailnet": {
        "form_id": "4. Trailnet",
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","pd-fish_farmer","trailnet-trailnet_date","trailnet-species_trailnet","trailnet-Catla_length_mm","trailnet-Ragandi_length_mm","trailnet-Mosu_length_mm","trailnet-Bangaru_papa_length_mm","trailnet-Grasscarp_length_mm","trailnet-Others_name","trailnet-Others_length_mm","trailnet-Catla_weight_grams","trailnet-Ragandi_weight_grams","trailnet-Mosu_weight_grams","trailnet-Bangaru_papa_weight_grams","trailnet-Grasscarp_weight_grams"],
        "district_col": "pd.district"
    },
    "Meetings&Trainings": {
        "form_id": "Capacity_building",
        "columns": ["CB_info.landscape","CB_info.gp","CB_info.village","CB_info.Trainining_type","CB_info.Event_name","CB_info.Event_mode","Cb_info1.from_date","Cb_info1.days","Cb_info1.male","Cb_info1.female","Cb_info1.total_members","Cb_info1.Event_place"],
        "landscape_col": "CB_info.landscape"
    },
    "Intensification of Orchards": {
        "form_id": "Orchards_Intensification",
        "columns": ["SubmissionDate","basic_info.landscape","basic_info.gp","basic_info.village","basic_info.orchard_type","basic_info.farmer_add","type"],
        "landscape_col": "basic_info.landscape"
    },
    "Agri Service Centers": {
        "form_id": "Agri Service Centers",
        "columns": ["SubmissionDate","pd.landscape","pd.gp","pd.village","farm_equipmnt_hired","ASC_Entp","ud.chc_equipmnt_rented_date","ud.chc_equipmnt_hired_farmer","ud.chc_equipmnt_total_hours_used","ud.total_hired_cost"],
        "landscape_col": "pd.landscape"
    },
    "Large & Small Ruminants": {
        "form_id": "Large_Small_Ruminants",
        "columns": ["table_list_df.Month","table_list_df.Monthly_MIS","table_list_df.landscape","table_list_df.gp","table_list_df.village","table_list_df.livestock_type","table_list_df.Farmer"],
        "landscape_col": "table_list_df.landscape"
    } 
}

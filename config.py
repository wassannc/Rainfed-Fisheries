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
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","pd.fish_farmer","trailnet.trailnet_date","trailnet.species_trailnet","trailnet.Catla_length_mm","trailnet.Ragandi_length_mm","trailnet.Mosu_length_mm","trailnet.Bangaru_papa_length_mm","trailnet.Grasscarp_length_mm","trailnet.Others_name","trailnet.Others_length_mm","trailnet.Catla_weight_grams","trailnet.Ragandi_weight_grams","trailnet.Mosu_weight_grams","trailnet.Bangaru_papa_weight_grams","trailnet.Grasscarp_weight_grams"],
        "district_col": "pd.district"
    },
    "5. Harvesting": {
        "form_id": "5. Harvesting",
        "columns": ["pd.date","pd.district","pd.block","pd.panchayat","pd.village","pd.fish_farmer","harvest.harvest_date","harvest.fish_avg_weight_kgs","harvest.fish_feed_expenses_rs","harvest.fish_sold_kgs","harvest.fish_solf_rate_per_kg","harvest.fish_sold_income","harvest.fish_own_consumption","harvest.fish_distributed_relatives"],
        "district_col": "pd.district"
    }
}

FORMS = {
    "Farmer Register": {
        "form_id": "FarmerRegister_NF",
        "columns": ["plot_reg.date","plot_reg.landscape","plot_reg.gp","plot_reg.village","plot_reg.farmer_name","plot_reg.spouse","plot_reg.season","plot_reg.crop_model","plot_reg.main_crop","plot_reg.sowing_date"],
        "landscape_col": "plot_reg.landscape"
    },
    "Activities": {
        "form_id": "Activities-NF",
        "columns": ["Primary_details.date","Primary_details.landscape","Primary_details.gp","Primary_details.village","Primary_details.farmer_name","Primary_details.plot_ext","crop_activity","Nf_activites.nf_inputs","Nf_activites.Other_nf_input","Nf_activites.Qty_other_nfinput"],
        "landscape_col": "Primary_details.landscape"
    },
    "BRC": {
        "form_id": "BRC_Units",
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.brc_unit","table_list_pd.product_name","table_list_pd.brc_sale_date","table_list_pd.dj_sale_farmer","table_list_pd.gender","table_list_pd.sale_village","table_list_sd.sale_qty","table_list_sd.total_income","table_list_cd.crops","table_list_cd.crop_ext"],
        "landscape_col": "table_list_pd.landscape"
    },
    "Micro Enterprizes": {
        "form_id": "Micro Enterprizes",
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.gp","table_list_pd.village","table_list_pd1.farmer_name","table_list_pd1.processing_hub_tool","table_list_pd1.processing_date","table_list_pd1.processed_for","table_list_pd2.processing_farmer_village","table_list_pd2.processing_farmer","table_list_pd2.processing_qty_kgs","table_list_pd2.rent_amount","table_list_pd3.Data_sub_by"],
        "landscape_col": "table_list_pd.landscape"
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

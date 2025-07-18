import streamlit as st
import pandas as pd
from helpers import *


summer,winter = data_preprocessor()

summer.dropna(subset=["region"], inplace=True)
winter.dropna(subset=["region"], inplace=True)
medal_count = summer.groupby(["Year","region","Medal"]).size().unstack(fill_value=0)

summer,winter = duplicate_rows_remover(summer,winter)


st.sidebar.title("MENU")
season = st.sidebar.radio("Choose Season :",( "Summer" , "Winter"))
options = st.sidebar.radio("Options" ,("Medal-Tally" , "Country-Wise" ,"Year-Wise" , "Year-Wise Progress"))

## MEDAL TALLY 
if season=="Summer" and options=="Medal-Tally":
    st.subheader("Summer Olympic Medal Tally")
    medal_pivot_summer = medals_tally_calculator(summer)
    medal_pivot_summer =  medal_pivot_summer .sort_values(by=["Gold" , "Silver" , "Bronze"] , ascending=False)
    st.dataframe(medal_pivot_summer , width=700)

elif season=="Winter" and options=="Medal-Tally":
    st.subheader("Winter Olympic Medal Tally")
    medal_pivot_winter= medals_tally_calculator(winter)
    medal_pivot_winter =  medal_pivot_winter.sort_values(by=["Gold" , "Silver" , "Bronze"] , ascending=False)
    st.dataframe(medal_pivot_winter , width=700)

### Country-wise

elif season=="Summer" and options=="Country-Wise":
    st.subheader("Summer Country Wise ")
    medal_pivot_summer = medals_tally_calculator(summer)
    noc = st.selectbox("Select NOC:" , medal_pivot_summer.index.tolist())
    details = country_wise_search(noc,medal_pivot_summer)
    table = pd.DataFrame.from_dict(details , orient="index" , columns=["Value"])
    st.dataframe(table)

### Country-wise winter

elif season=="Winter" and options=="Country-Wise":
    st.subheader("Winter Country Wise ")
    medal_pivot_winter = medals_tally_calculator(winter)
    noc = st.selectbox("Select NOC:" , medal_pivot_winter.index.tolist())
    details = country_wise_search(noc,medal_pivot_winter)
    table = pd.DataFrame.from_dict(details , orient="index" , columns=["Value"])
    st.dataframe(table)


### YEAR WISE
elif season=="Summer" and options=="Year-Wise":
    st.subheader("Summer Year Wise")
    
    years = sorted(summer["Year"].unique())
    selected_year =st.selectbox("Select Year", years)

    countries = sorted(summer[summer["Year"]==selected_year]["region"].unique())
    selected_country = st.selectbox("Select Country:" ,countries)

    plot_medals(selected_year,selected_country,summer)






elif season=="Winter" and options=="Year-Wise":
    st.subheader("Winter Year Wise")
    
    years = sorted(winter["Year"].unique())
    selected_year =st.selectbox("Select Year", years)

    countries = sorted(winter[winter["Year"]==selected_year]["region"].unique())
    selected_country = st.selectbox("Select Country:" ,countries)

    plot_medals(selected_year,selected_country,winter)



## YEAR WISE PROGRESS 
elif season=="Summer" and options=="Year-Wise Progress":
    st.subheader("OVERALL ANALYSIS OF A COUNTRY")
    
    countries = sorted(summer["region"].unique())
    selected_country = st.selectbox("Choose country:" ,countries)
    year_analysis(selected_country,summer)

else:

    st.subheader("OVERALL ANALYSIS OF A COUNTRY")
    
    countries = sorted(winter["region"].unique())
    selected_country = st.selectbox("Choose country:" ,countries)
    year_analysis(selected_country,winter)
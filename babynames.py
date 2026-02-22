import streamlit as st
import pandas as pd
import numpy as np
import os
from io import StringIO

NEWEST_DATA = 2024
the_states = ["AK", "AL", "AR", "AZ", "CA", "CO",
            "CT", "DC", "DE", "FL", "GA", "HI",
            "IA", "ID", "IL", "IN", "KS", "KY",
            "LA", "MA", "MD", "ME", "MI", "MN",
            "MO", "MS", "MT", "NC", "ND", "NE",
            "NH", "NJ", "NM", "NV", "NY", "OH",
            "OK", "OR", "PA", "RI", "SC", "SD",
            "TN", "TX", "UT", "VA", "VT", "WA",
            "WV", "WY"]
all_states = []

class state_data:
    def __init__(self, state, name, births, percentage, relative):
        self.state = state
        self.name = name
        self.births = births
        self.percentage = percentage
        self.relative = relative

    def __repr__(self):
        return f"State(name='{self.name}', births={self.births})"    

# Popularity of a name
def home():
    st.title("Baby Names Popularity")
    st.write("Enter a name to see how popular it was in a given year.")

    # Ensures that the name data only shows up after the name has been input
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # Define the 2 columns
    col1, col2 = st.columns(2, border=True)

    # Column 1 contains the name text box
    with col1:
        my_name = st.text_input(
                "Name:",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Your name",
            )

    # Column 2 contains the year and sex
    with col2:
        year = st.number_input(
        label="Date (1880-2024):",
        min_value=1880,
        max_value=NEWEST_DATA,
        value=NEWEST_DATA,  # defaults to the most recent year with data
        step=1  # only whole numbers, no decimals!
        )

        sex = st.radio(
        label="Sex:",
        options=["Male","Female"]    
        )

    # Output after inputting the name
    if my_name:
        try:
            my_name = my_name.title() # convert the input to title case (only the first letter is capitalized)
            st.write(f"**Data on the name {my_name}**")
            
            # get the current directory and find the data with the given year
            current_dir = os.getcwd()
            df = pd.read_csv(current_dir + '\\names\\yob' + str(year) + '.csv')

            # see how many babies were given the name
            girls = df[(df['Name'] == my_name) & (df['Sex'] == "F")]
            if (not girls.empty):
                girls_count = girls['Births'].values[0]
                girls_rank = girls['Ranking'].values[0]

            boys = df[(df['Name'] == my_name) & (df['Sex'] == "M")]
            if (not boys.empty):
                boys_count = boys['Births'].values[0]
                boys_rank = boys['Ranking'].values[0]

            # display data if the user chose male or female
            if (sex == "Male"):
                if (boys.empty):
                    st.write("Less than 5 boys were named ", my_name, " in " , str(year), ".")
                else:
                    st.write(str(boys_count), " boys were named ", my_name, " in " , str(year), ". It was the #", str(boys_rank), "boy's name.")
                    #st.write(my_name, "was the #", str(boys_rank), "boy's name")

            elif (sex == "Female"):
                if (girls.empty):
                    st.write("Less than 5 girls were named ", my_name, " in " , str(year), ".")
                else:
                    st.write(str(girls_count), " girls were named ", my_name, " in " , str(year), ". It was the #", str(girls_rank), "girl's name.")
                    #st.write(my_name, "was the #", str(girls_rank), "girl's name")

        # shows message if data file doesn't exist
        except FileNotFoundError:
            st.write("Data for that year doesn't exist... not yet, at least.")

# Name prefixes and suffixes
def data_page():
    st.title("Beginnings and Endings")
    st.write("See how many names in a given year's data begin or end with certain letters.")

    # Ensures that the name data only shows up after the name has been input
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # Define the 2 columns
    col1, col2 = st.columns(2, border=True)

    # Column 1 contains the wanted letters
    with col1:
        letters = st.text_input(
                "Name:",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Prefix/suffix",
            )

    # Column 2 contains the year, sex, and whether the wanted letters are a prefix or suffix
    with col2:
        year = st.number_input(
        label="Date (1880-2024):",
        min_value=1880,
        max_value=NEWEST_DATA,
        value=NEWEST_DATA,  # defaults to the most recent year with data
        step=1  # only whole numbers, no decimals!
        )

        sex = st.radio(
        label="Sex:",
        options=["Male","Female"]    
        )

        location = st.radio(
        label="Location:",
        options=["Prefix","Suffix"]    
        )

    # convert prefixes to title case and suffixes to lowercase
    if letters:
        if (location == "Prefix"):
            letters = letters.title()
        else:
            letters = letters.lower()
    
        #st.write("You entered", letters)

        current_dir = os.getcwd()
        df = pd.read_csv(current_dir + '\\names\\yob' + str(year) + '.csv')

        if (location == "Prefix"):
            st.write("Names beginning with", letters)
            if (sex == "Male"):
                filtered_df = df[df['Name'].str.startswith(letters) & (df['Sex'] == 'M')]
                st.dataframe(filtered_df, hide_index=True, column_config={"Sex": None})
            else:
                filtered_df = df[df['Name'].str.startswith(letters) & (df['Sex'] == 'F')]
                st.dataframe(filtered_df, hide_index=True, column_config={"Sex": None})

        elif (location == "Suffix"):
            st.write("Names ending with", letters)
            if (sex == "Male"):
                filtered_df = df[df['Name'].str.endswith(letters) & (df['Sex'] == 'M')]
                st.dataframe(filtered_df, hide_index=True, column_config={"Sex": None})
            else:
                filtered_df = df[df['Name'].str.endswith(letters) & (df['Sex'] == 'F')]
                st.dataframe(filtered_df, hide_index=True, column_config={"Sex": None})

# Popularity of a name by state
def bystate():
    st.title("Name Popularity by State")
    st.write("Enter a name to see how popular it was in a given year in each state.")

    # Ensures that the name data only shows up after the name has been input
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # Define the 2 columns
    col1, col2 = st.columns(2, border=True)

    # Column 1 contains the name text box
    with col1:
        my_name = st.text_input(
                "Name:",
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Your name",
            )

    # Column 2 contains the year and sex
    with col2:
        year = st.number_input(
        label="Date (1910-2024):",
        min_value=1910,
        max_value=NEWEST_DATA,
        value=NEWEST_DATA,  # defaults to the most recent year with data
        step=1  # only whole numbers, no decimals!
        )

        sex = st.radio(
        label="Sex:",
        options=["Male","Female"]    
        )

    # Output after inputting the name
    if my_name:
        try:
            my_name = my_name.title() # convert the input to title case (only the first letter is capitalized)
            st.write(f"**Data on the name {my_name}**")
            
            # get the current directory and find the data with the given year
            current_dir = os.getcwd()
            df = pd.read_csv(current_dir + '\\names\\yob' + str(year) + '.csv')

            # see how many babies were given the name
            girls = df[(df['Name'] == my_name) & (df['Sex'] == "F")]
            if (not girls.empty):
                girls_count = girls['Births'].values[0]
                girls_rank = girls['Ranking'].values[0]

            boys = df[(df['Name'] == my_name) & (df['Sex'] == "M")]
            if (not boys.empty):
                boys_count = boys['Births'].values[0]
                boys_rank = boys['Ranking'].values[0]

            # display data if the user chose male or female
            if (sex == "Male"):
                if (boys.empty):
                    st.write("Less than 5 boys were named ", my_name, " in " , str(year), ".")
                else:
                    st.write(str(boys_count), " boys were named ", my_name, " in " , str(year), ".")
                    st.write("Here is the state-by-state (plus DC) breakdown.")
                    st.write("This may take a few seconds to load.")
                    
                    for state in the_states:
                        temp_df = pd.read_csv(current_dir + '\\namesbystate\\' + state + '.csv')

                        total_babies = temp_df[(temp_df['Year'] == year) & 
                        (temp_df['Name'] == my_name) & 
                        (temp_df['Sex'] == "M")]['Births'].sum()

                        perc = float(float(total_babies) / float(boys_count))*100
                        total = temp_df.loc[(temp_df['Sex'] == "M") & (temp_df['Year'] == year), 'Births'].sum()
                        relat = float(total_babies / total) * 100

                        entry = state_data(state, my_name, total_babies, perc, relat)
                        all_states.append(entry)

                        
                        final_df = pd.DataFrame([vars(s) for s in all_states]) 
                    
                    st.dataframe(final_df, hide_index=True, column_config={"name": None})
                                      

            elif (sex == "Female"):
                if (girls.empty):
                    st.write("Less than 5 girls were named ", my_name, " in " , str(year), ".")
                else:
                    st.write(str(girls_count), " girls were named ", my_name, " in " , str(year), ".")
                    st.write("Here is the state-by-state (plus DC) breakdown:")
                    st.write("This may take a few seconds to load.")
                    
                    for state in the_states:
                        temp_df = pd.read_csv(current_dir + '\\namesbystate\\' + state + '.csv')

                        total_babies = temp_df[(temp_df['Year'] == year) & 
                        (temp_df['Name'] == my_name) & 
                        (temp_df['Sex'] == "F")]['Births'].sum()

                        perc = float(float(total_babies) / float(girls_count))*100
                        total = temp_df.loc[(temp_df['Sex'] == "F") & (temp_df['Year'] == year), 'Births'].sum()
                        relat = float(total_babies / total) * 100

                        entry = state_data(state, my_name, total_babies, perc, relat)
                        all_states.append(entry)

                        
                        final_df = pd.DataFrame([vars(s) for s in all_states]) 
                        
                    st.dataframe(final_df, hide_index=True, column_config={"name": None})

        # shows message if data file doesn't exist
        except FileNotFoundError:
            st.write("Data for that year doesn't exist... not yet, at least.")


pg = st.navigation([
    st.Page(home, title="Popularity", icon="📊", default=True),
    st.Page(data_page, title="Beginnings and Endings", icon="🅱️"),
    st.Page(bystate, title="Popularity by State", icon="🗺️")
])

pg.run()



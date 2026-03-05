#Imports

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_excel(self.file_path)
        print(f"Loaded {len(self.data)} rows.")

    def summarize(self):
        if self.data is not None:
            return self.data.info()     
        
    def transformation(self):

        #----------SaleDate----------
        print('Addressing abnomal inputs in SaleDate ...')
        self.data["SaleDate"]=pd.to_datetime(self.data["SaleDate"],format="%d/%m/%Y",errors='coerce')
        self.data["FormattedDate"] = self.data["SaleDate"].dt.strftime("%d/%m/%Y")
        
        #----------PropertyAddress----------
        print("Initializing the clea-up of 'PropertyAddress' column ...")
        # 1. Create the lookup map ONCE for the whole dataset
        # Mapping ParcelID -> PropertyAddress (only using rows that HAVE an address)
        lookup_map = (
            self.data.dropna(subset=['PropertyAddress'])
            .drop_duplicates('ParcelID')
            .set_index('ParcelID')['PropertyAddress']
        )

        print("Processing for null values ...")
        # 2. Identify rows that need fixing
        # Condition: Address is NaN AND ParcelID is not NaN
        mask = self.data['PropertyAddress'].isna() & self.data['ParcelID'].notna()

        print("Fetching the right address value for the missing address ...")
        # 3. Apply the fix using .map()
        # This looks up the ParcelID in our lookup_map and fills the NaN
        self.data.loc[mask, 'PropertyAddress'] = self.data.loc[mask, 'PropertyAddress'].fillna(
            self.data['ParcelID'].map(lookup_map)
        )

        #----------SoldAsVacant----------
        print('Addressing abnomal inputs in SoldAsVacant ...')
        replacement = {'Y': 'Yes', 'N': 'No'}

        self.data['SoldAsVacant'] = (
            self.data['SoldAsVacant'].
            map(replacement).
            fillna(self.data['SoldAsVacant'])
            )
        
        #----------City----------
        print('Extracting information from the address')
        # Regex Pattern
        # (.*)    : First capturing group (Address) - greedy match up to the last comma
        # ,       : The separator comma
        # \s* : Ignore any whitespace after the comma
        # (.*)    : Second capturing group (City)
        
        pattern= r'(.*),\s*(.*)'
        self.data[['address','city']]= self.data['PropertyAddress'].str.extract(pattern)
        
class analyzer:
    
    def __init__(self,path):
        # 1. Create the processor
        self.processor = DataProcessor(path)

        # 2. Trigger the processor to actually do the work
        self.processor.load_data()
        self.processor.transformation()

        # 3. Create a shortcut to the data for easy access
        self.data = self.processor.data
        

    def summarize(self):
        if self.data is not None:
            print("\n--- Data Summary Post Transformation ---")
            return self.data.info() 
        else:
            return "No data found to summarize."
        
    def cleanup(self):
        print("Removing duplicate records...")
        self.data.drop_duplicates(subset=['UniqueID '], keep='first', inplace=True)

    def a1(self):
        #Creating copy of the required fields for analysis
        a1_df=self.data[['FormattedDate','LandValue','BuildingValue','Acreage','SalePrice','city']]

        # Calculate Land Value per Acre
        a1_df['LandValuePerAcre'] = a1_df['LandValue'] / a1_df['Acreage'].replace(0, np.nan)

        #Extracting year from FormattedDate
        a1_df['Year']=pd.to_datetime(self.data['FormattedDate'], dayfirst=True, errors='coerce').dt.year
        
        #Aggregate the results for analysis
        trend_data = a1_df.groupby(['Year', 'city'])[['LandValuePerAcre', 'BuildingValue', 'SalePrice']].mean().reset_index()

        # Set up the visual style
        sns.set_theme(style="whitegrid")

        # --- GRAPH 1: Land Value per Acre Trend ---
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=trend_data, 
            x='Year', 
            y='LandValuePerAcre', 
            hue='city',       # Different line for each city
            marker='o',       # Circular data points
            markersize=8,     # Size of the points
            linewidth=2.5     # Thickness of the lines
        )
        plt.title('Average Land Value per Acre Trend by City', fontsize=14)
        plt.ylabel('Value per Acre ($)')
        plt.xticks(trend_data['Year'].unique()) # Ensures every year is shown on axis
        plt.savefig('plots/land_value_line_trend.png')

        # --- GRAPH 2: Building Value Trend ---
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=trend_data, 
            x='Year', 
            y='BuildingValue', 
            hue='city',       # Different line for each city
            marker='s',       # Square data points (distinct from the other graph)
            markersize=8, 
            linewidth=2.5
        )
        plt.title('Average Building Value Trend by City', fontsize=14)
        plt.ylabel('Building Value ($)')
        plt.xticks(trend_data['Year'].unique())
        plt.savefig('plots/building_value_line_trend.png')

        # --- VISUALIZATION 2: Building Value vs Sale Price ---
        # We melt the data to compare two different dollar metrics (Sale vs Building) side-by-side
        comparison_df = trend_data.melt(id_vars=['Year', 'city'], 
                                        value_vars=['SalePrice', 'BuildingValue'], 
                                        var_name='Metric', value_name='Amount')

        # Catplot creates a grid of bar charts (one per city)
        g = sns.catplot(data=comparison_df, kind="bar", x="Year", y="Amount", hue="Metric", col="city", height=5, aspect=1.2)
        g.set_axis_labels("Year", "Market Value ($)")
        g.fig.suptitle('Sale Price vs Building Value Trend per City', y=1.05)
        plt.savefig('plots/sale_vs_building_trend.png')

    def a2(self):
        #Creating copy of the required fields for analysis
        a1_df=self.data[['FormattedDate','LandValue','BuildingValue','Acreage','SalePrice','TaxDistrict']]

        # Calculate Land Value per Acre
        a1_df['LandValuePerAcre'] = a1_df['LandValue'] / a1_df['Acreage'].replace(0, np.nan)

        #Extracting year from FormattedDate
        a1_df['Year']=pd.to_datetime(self.data['FormattedDate'], dayfirst=True, errors='coerce').dt.year
        
        #Aggregate the results for analysis
        trend_data = a1_df.groupby(['Year', 'TaxDistrict'])[['LandValuePerAcre', 'BuildingValue', 'SalePrice']].mean().reset_index()

        # Set up the visual style
        sns.set_theme(style="whitegrid")

        # --- GRAPH 1: Land Value per Acre Trend ---
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=trend_data, 
            x='Year', 
            y='LandValuePerAcre', 
            hue='TaxDistrict',       # Different line for each city
            marker='o',       # Circular data points
            markersize=8,     # Size of the points
            linewidth=2.5     # Thickness of the lines
        )
        plt.title('Average Land Value per Acre Trend by TaxDistrict', fontsize=14)
        plt.ylabel('Value per Acre ($)')
        plt.xticks(trend_data['Year'].unique()) # Ensures every year is shown on axis
        plt.savefig('plots/land_value_line_trend_TaxDistrict.png')  

        # --- GRAPH 2: Building Value Trend ---
        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=trend_data, 
            x='Year', 
            y='BuildingValue', 
            hue='TaxDistrict',       # Different line for each TaxDistrict
            marker='s',       # Square data points (distinct from the other graph)
            markersize=8, 
            linewidth=2.5
        )
        plt.title('Average Building Value Trend by TaxDistrict', fontsize=14)
        plt.ylabel('Building Value ($)')
        plt.xticks(trend_data['Year'].unique())
        plt.savefig('plots/building_value_line_trend_TaxDistrict.png')

        # --- VISUALIZATION 2: Building Value vs Sale Price ---
        # We melt the data to compare two different dollar metrics (Sale vs Building) side-by-side
        comparison_df = trend_data.melt(id_vars=['Year', 'TaxDistrict'], 
                                        value_vars=['SalePrice', 'BuildingValue'], 
                                        var_name='Metric', value_name='Amount')

        # Catplot creates a grid of bar charts (one per city)
        g = sns.catplot(data=comparison_df, kind="bar", x="Year", y="Amount", hue="Metric", col="TaxDistrict", height=5, aspect=1.2)
        g.set_axis_labels("Year", "Market Value ($)")
        g.fig.suptitle('Sale Price vs Building Value Trend per TaxDistrict', y=1.05)
        plt.savefig('plots/sale_vs_building_trend_TaxDistrict.png')




def helper_function():
        print("Preparing to process...")

        


# --- THE EXECUTION ZONE ---
def main():
    helper_function()
    
    # Initialize the path
    path="data/Nashville Housing Data for Data Cleaning.xlsx"
    
    analyze=analyzer(path)
    print(analyze.summarize())

    # Call the visualization method
    print("Generating trend graphs...")
    analyze.a1()
    analyze.a2()

if __name__ == "__main__":
    main()


    
import pandas as pd

# Spectral Bands data
spectral_bands = [
    {"Name": "AOT", "Common Name": None, "GSD": None, "Center Wavelength": None, "Full Width Half Maximum": None, "Description": "Aerosol optical thickness"},
    {"Name": "B01", "Common Name": "coastal", "GSD": "60 m", "Center Wavelength": "0.443 μm", "Full Width Half Maximum": "0.027 μm", "Description": "Coastal aerosol"},
    {"Name": "B02", "Common Name": "blue", "GSD": "10 m", "Center Wavelength": "0.49 μm", "Full Width Half Maximum": "0.098 μm", "Description": "Visible blue"},
    {"Name": "B03", "Common Name": "green", "GSD": "10 m", "Center Wavelength": "0.56 μm", "Full Width Half Maximum": "0.045 μm", "Description": "Visible green"},
    {"Name": "B04", "Common Name": "red", "GSD": "10 m", "Center Wavelength": "0.665 μm", "Full Width Half Maximum": "0.038 μm", "Description": "Visible red"},
    {"Name": "B05", "Common Name": "rededge", "GSD": "20 m", "Center Wavelength": "0.704 μm", "Full Width Half Maximum": "0.019 μm", "Description": "Vegetation classification red edge"},
    {"Name": "B06", "Common Name": "rededge", "GSD": "20 m", "Center Wavelength": "0.74 μm", "Full Width Half Maximum": "0.018 μm", "Description": "Vegetation classification red edge"},
    {"Name": "B07", "Common Name": "rededge", "GSD": "20 m", "Center Wavelength": "0.783 μm", "Full Width Half Maximum": "0.028 μm", "Description": "Vegetation classification red edge"},
    {"Name": "B08", "Common Name": "nir", "GSD": "10 m", "Center Wavelength": "0.842 μm", "Full Width Half Maximum": "0.145 μm", "Description": "Near infrared"},
    {"Name": "B8A", "Common Name": "rededge", "GSD": "20 m", "Center Wavelength": "0.865 μm", "Full Width Half Maximum": "0.033 μm", "Description": "Vegetation classification red edge"},
    {"Name": "B09", "Common Name": None, "GSD": "60 m", "Center Wavelength": "0.945 μm", "Full Width Half Maximum": "0.026 μm", "Description": "Water vapor"},
    {"Name": "B11", "Common Name": "swir16", "GSD": "20 m", "Center Wavelength": "1.61 μm", "Full Width Half Maximum": "0.143 μm", "Description": "Short-wave infrared, snow/ice/cloud classification"},
    {"Name": "B12", "Common Name": "swir22", "GSD": "20 m", "Center Wavelength": "2.19 μm", "Full Width Half Maximum": "0.242 μm", "Description": "Short-wave infrared, snow/ice/cloud classification"},
]

# Item-Level Assets data
item_level_assets = [
    {"Title": "Aerosol optical thickness (AOT)", "STAC Key": "AOT", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": None},
    {"Title": "Band 1 - Coastal aerosol - 60m", "STAC Key": "B01", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "60 m", "Spectral Bands": "B01 (coastal)"},
    {"Title": "Band 2 - Blue - 10m", "STAC Key": "B02", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": "B02 (blue)"},
    {"Title": "Band 3 - Green - 10m", "STAC Key": "B03", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": "B03 (green)"},
    {"Title": "Band 4 - Red - 10m", "STAC Key": "B04", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": "B04 (red)"},
    {"Title": "Band 5 - Vegetation red edge 1 - 20m", "STAC Key": "B05", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B05 (rededge)"},
    {"Title": "Band 6 - Vegetation red edge 2 - 20m", "STAC Key": "B06", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B06 (rededge)"},
    {"Title": "Band 7 - Vegetation red edge 3 - 20m", "STAC Key": "B07", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B07 (rededge)"},
    {"Title": "Band 8 - NIR - 10m", "STAC Key": "B08", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": "B08 (nir)"},
    {"Title": "Band 9 - Water vapor - 60m", "STAC Key": "B09", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "60 m", "Spectral Bands": "B09"},
    {"Title": "Band 11 - SWIR (1.6) - 20m", "STAC Key": "B11", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B11 (swir16)"},
    {"Title": "Band 12 - SWIR (2.2) - 20m", "STAC Key": "B12", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B12 (swir22)"},
    {"Title": "Band 8A - Vegetation red edge 4 - 20m", "STAC Key": "B8A", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": "B8A (rededge)"},
    {"Title": "Scene classification map (SCL)", "STAC Key": "SCL", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "20 m", "Spectral Bands": None},
    {"Title": "Water vapor (WVP)", "STAC Key": "WVP", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": None},
    {"Title": "True color image", "STAC Key": "visual", "Roles": "Data", "Type": "GeoTIFF (COG)", "GSD": "10 m", "Spectral Bands": "B04 (red), B03 (green), B02 (blue)"},
    {"Title": "Thumbnail", "STAC Key": "preview", "Roles": "Thumbnail", "Type": "GeoTIFF (COG)", "GSD": None, "Spectral Bands": None},
    {"Title": "SAFE manifest", "STAC Key": "safe-manifest", "Roles": "Metadata", "Type": "XML", "GSD": None, "Spectral Bands": None},
    {"Title": "Granule metadata", "STAC Key": "granule-metadata", "Roles": "Metadata", "Type": "XML", "GSD": None, "Spectral Bands": None},
    {"Title": "INSPIRE metadata", "STAC Key": "inspire-metadata", "Roles": "Metadata", "Type": "XML", "GSD": None, "Spectral Bands": None},
    {"Title": "Product metadata", "STAC Key": "product-metadata", "Roles": "Metadata", "Type": "XML", "GSD": None, "Spectral Bands": None},
    {"Title": "Datastrip metadata", "STAC Key": "datastrip metadata", "Roles": "Metadata", "Type": "XML", "GSD": None, "Spectral Bands": None},
]

# Preprocessing function for Spectral Bands
def clean_spectral_bands(data):
    cleaned_data = []
    for entry in data:
        entry['Common Name'] = entry['Common Name'] if entry['Common Name'] else 'Unknown' # Handle missing Common Name (replace None with 'Unknown')
        entry['GSD'] = entry['GSD'] if entry['GSD'] else 'Unknown' # Handle missing GSD (replace None with 'Unknown')
        if entry['Center Wavelength']: # Normalize the Center Wavelength and GSD by removing units for numerical calculations (remove 'μm' and 'm')
            entry['Center Wavelength'] = float(entry['Center Wavelength'].replace(' μm', ''))
        if entry['GSD'] != 'Unknown':
            entry['GSD'] = entry['GSD'].replace(' m', '')
        cleaned_data.append(entry)
    return cleaned_data

# Preprocessing function for Item-Level Assets
def clean_item_level_assets(data):
    cleaned_data = []
    for entry in data:
        entry['Spectral Bands'] = entry['Spectral Bands'] if entry['Spectral Bands'] else 'Unknown' # Handle missing Spectral Bands (replace None with 'Unknown')
        entry['GSD'] = entry['GSD'] if entry['GSD'] else 'Unknown' # Handle missing GSD (replace None with 'Unknown')
        # Normalize GSD (remove 'm')
        if entry['GSD'] != 'Unknown': 
            entry['GSD'] = entry['GSD'].replace(' m', '')
        cleaned_data.append(entry)
    return cleaned_data

# Clean the data for both sections
cleaned_spectral_bands = clean_spectral_bands(spectral_bands)
cleaned_item_level_assets = clean_item_level_assets(item_level_assets)

# Convert both cleaned datasets into Pandas DataFrames for easy handling
df_cleaned_spectral_bands = pd.DataFrame(cleaned_spectral_bands)
df_cleaned_item_level_assets = pd.DataFrame(cleaned_item_level_assets)

# Print cleaned data
print("Cleaned Spectral Bands Data:")
print(df_cleaned_spectral_bands)

print("\nCleaned Item-Level Assets Data:")
print(df_cleaned_item_level_assets)
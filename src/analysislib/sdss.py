# Import necessary libraries
import pandas as pd

# Define setup function to clean and prepare the data
def setup(df):
    df = df[df["zWarning"] == 0] # Set the dataframe to only include instances where zWarning was 0

    photometry_bands = ["u", "g", "r", "i", "z"] # Define a list of all the photometry bands

    # Loop through every passband and check if the value is OK
    for band in photometry_bands:
        df = df[df[band] > 0]

    # Separate dataframe
    global galaxies
    global stars
    global qsos
    
    galaxies = df[df["class"] == "GALAXY"]
    stars = df[df["class"] == "STAR"]
    qsos = df[df["class"] == "QSO"]

    # Remove galaxies with zero or negative values
    galaxies = galaxies[(galaxies["petroRad_r"] > 0) & (galaxies["fracDeV_r"] > 0)]

    # Drop unnecessary columns
    stars = stars.drop(columns=["petroRad_r", "petroMag_r", "fracDeV_r", "expRad_r", "deVRad_r", "expAB_r", "deVAB_r"])
    qsos = qsos.drop(columns=["petroRad_r", "petroMag_r", "fracDeV_r", "expRad_r", "deVRad_r", "expAB_r", "deVAB_r"])

# Return the three dataframes
def _galaxies():
    return galaxies

def _stars():
    return stars

def _qsos():
    return qsos

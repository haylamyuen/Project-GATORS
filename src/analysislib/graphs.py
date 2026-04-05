# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import plotly.express as px

# Setup wavelength range and rest wavelength for H-alpha line
wavelength = np.linspace(300, 2500, 3000)
REST_WL = 656.3 # Rest Wavelength
def gauss(x, mu):
    return np.exp(-((x - mu)**2)/(2*8**2))

# Start interactive plotting
def plot_redshift(z):
    shifted_wl = REST_WL*(1+z) # Define shifted wavelength
    fig, ax = plt.subplots(figsize=(18, 4), facecolor="#1e1e1e")
    ax.set_facecolor("#1e1e1e")

    # Plot original line
    ax.fill_between(wavelength, gauss(wavelength, REST_WL), alpha=0.12, color="white")
    ax.plot(wavelength, gauss(wavelength, REST_WL), "--", lw=1, alpha=0.35, color="white")

    # Plot shifted line
    ax.fill_between(wavelength, gauss(wavelength, shifted_wl), alpha=0.35, color="#ff5555")
    ax.plot(wavelength, gauss(wavelength, shifted_wl), lw=2.5, color="#ff5555", label=f"H-alpha: {REST_WL:.0f} nm --> {shifted_wl:.0f} nm")

    # Set plot aesthetics
    ax.set_title(f"z = {z:.2f}  |  stretched by {z*100:.0f}%  |  ~{round(z*13800):,} million light-years", color="#cccccc", fontsize=12, loc="left", pad=8)
    ax.set_xlabel("Wavelength (nm)", color="#aaaaaa", fontsize=9)
    ax.set_xlim(300, 2500)
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    ax.tick_params(colors="#777777", labelsize=10)
    ax.grid(True, linestyle=":", alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    ax.legend(facecolor="#2a2a2a", edgecolor="#444444", labelcolor="#e0e0e0", fontsize=10)
    plt.tight_layout()
    plt.show()

# Create interactive slider for redshift
z_slider = widgets.FloatSlider(value=0.0, min=0.0, max=2.5, step=0.01, description="Redshift z =", continuous_update=True, layout=widgets.Layout(width="90%"), style={"description_width": "initial"})
out = widgets.interactive_output(plot_redshift, {"z": z_slider})

# Redshift Plot Function
def interactive_redshift():
    display(widgets.VBox([z_slider], layout=widgets.Layout(padding="2px 0")), out)

# Preliminary Plots Function
def prelim_plots(df):
    # Setup for plotting
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Pie chart for class distribution
    class_counts = df["class"].value_counts()
    colours = ["#5588dd", "#dd8855", "#dd5555"]
    df["class"].value_counts().plot.pie(autopct="%1.1f%%", ax=axes[0], startangle=90, color=colours)
    axes[0].set_title("Object Type Distribution")
    axes[0].set_ylabel("")

    # Redshift distribution histogram
    galaxy_z = df.loc[df["class"] == "GALAXY", "redshift"]
    qso_z = df.loc[df["class"] == "QSO", "redshift"]
    axes[1].hist(galaxy_z, bins=60, range=(0, 4), color="#5588dd", alpha=0.7, label=f"Galaxies (median z = {galaxy_z.median():.2f})")
    axes[1].hist(qso_z, bins=60, range=(0, 4), color="#dd8855", alpha=0.7, label=f"QSOs (median z = {qso_z.median():.2f})")
    axes[1].set_xlabel("Redshift (z)")
    axes[1].set_ylabel("Count")
    axes[1].set_title("Redshift Distribution: Galaxies vs QSOs", fontweight="bold", pad=12)
    axes[1].legend()

    # Overall title and display
    plt.suptitle("First Look at the SDSS Dataset", fontsize=20, fontweight="bold", y=1.05)
    plt.show()

# Sky Map Function
def sky_map(df):
    # Chose a 200,000 object sample
    df_sample = df.sample(min(len(df), 200000), random_state=67)

    # Use a scatter plot for the sky map
    fig = px.scatter(
        df_sample,
        x="ra",
        y="dec",
        color="class",
        color_discrete_map={"GALAXY": "#5588dd", "STAR": "#dd8855", "QSO": "#ff5555"},
        labels={"ra": "Right Ascension (degrees)", "dec": "Declination (degrees)", "class": "Object class"},
        title="Sky Map of SDSS Objects"
    )
    fig.update_traces(marker=dict(size=2, opacity=0.6))

    # Style the plot
    fig.update_layout(
        template=None,
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(family="monospace", size=12, color="#e0e0e0"),
        title_font=dict(family="monospace", size=18, color="#e0e0e0"),
        xaxis=dict(showgrid=True, gridcolor="#444444", zeroline=False, title_font=dict(size=13), tickcolor="#cccccc"),
        yaxis=dict(showgrid=True, gridcolor="#444444", zeroline=False, title_font=dict(size=13), tickcolor="#cccccc"),
        width=1000, height=450,
        legend=dict(bgcolor="#2a2a2a", bordercolor="#aaaaaa", borderwidth=1, font=dict(size=12, color="#e0e0e0"))
    )

    # Show the graph
    fig.show()
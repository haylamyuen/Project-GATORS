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

def hubble_fork():
    out = """
    <style>
    .tf-wrap { background:#0d0d14; border:1px solid #1e1e2e; border-radius:4px; padding:18px 12px 10px; font-family:'Courier New',monospace; }
    .tf-title { color:#9999bb; font-size:.78rem; letter-spacing:.1em; text-align:center; margin-bottom:14px; }
    .tf-row   { display:flex; align-items:center; justify-content:center; gap:0; position:relative; }
    .tf-arm   { display:flex; flex-direction:column; gap:18px; justify-content:center; margin-left:8px; }

    .gnode    { display:flex; flex-direction:column; align-items:center; cursor:pointer; padding:6px; border-radius:4px;
    border:1px solid transparent; transition:border-color .18s, filter .18s; }
    .gnode:hover, .gnode.active { border-color:#555577; filter:brightness(1.3) drop-shadow(0 0 6px rgba(180,180,255,.35)); }
    .gnode img { width:72px; height:72px; object-fit:cover; border-radius:3px; display:block; }
    .gnode .nl { font-size:9px; color:#8888aa; margin-top:4px; letter-spacing:.07em; }
    .arm-label { font-size:8px; color:#333348; letter-spacing:.06em; text-align:center; margin-bottom:2px; }

    .tf-panel  { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px; min-height:90px; }
    .tf-panel.empty { display:flex; align-items:center; justify-content:center; }
    .hint   { font-size:.72rem; color:#333344; letter-spacing:.06em; }

    .tf-name { font-size:.92rem; color:#d0d0e8; margin-bottom:5px; }
    .tf-tag  { display:inline-block; font-size:.62rem; letter-spacing:.08em; padding:1px 6px; border-radius:2px; margin-bottom:8px; }
    .tf-desc { font-size:.82rem; color:#9090a8; line-height:1.55; }
    .tf-sdss { margin-top:8px; font-size:.65rem; color:#444466; }
    .tf-stats { display:flex; flex-direction:column; gap:6px; }

    .srow   { display:flex; flex-direction:column; gap:2px; }
    .slabel { font-size:.62rem; color:#444455; letter-spacing:.07em; }
    .strack { height:4px; background:#1a1a2a; border-radius:2px; overflow:hidden; }
    .sbar   { height:100%; border-radius:2px; transition:width .45s cubic-bezier(.4,0,.2,1); }
    </style>

    <div class='tf-wrap'>
    <div class='tf-title'>THE HUBBLE TUNING FORK: Click any galaxy type</div>

    <div class='tf-row'>
        <!-- Ellipticals (left stem) -->
        <div style='display:flex;align-items:center;gap:4px;'>
        <div class='gnode' data-t='E0'><img src='images/hubble_fork/tf_E0.webp'><span class='nl'>E0</span></div>
        <div style='width:18px;height:1px;background:#22223a'></div>
        <div class='gnode' data-t='E3'><img src='images/hubble_fork/tf_E3.jpg'><span class='nl'>E3</span></div>
        <div style='width:18px;height:1px;background:#22223a'></div>
        <div class='gnode' data-t='E7'><img src='images/hubble_fork/tf_E7.jpg'><span class='nl'>E7</span></div>
        <div style='width:18px;height:1px;background:#22223a'></div>
        <div class='gnode' data-t='S0'><img src='images/hubble_fork/tf_S0.png'><span class='nl'>S0</span></div>
        </div>

        <!-- Fork split -->
        <svg width='30' height='180' style='flex-shrink:0;overflow:visible'>
        <line x1='0' y1='90' x2='15' y2='38' stroke='#22223a' stroke-width='1.2'/>
        <line x1='0' y1='90' x2='15' y2='142' stroke='#22223a' stroke-width='1.2'/>
        </svg>

        <!-- Two arms -->
        <div class='tf-arm'>
        <div class='arm-label'>normal spirals</div>
        <div style='display:flex;align-items:center;gap:4px;'>
            <div class='gnode' data-t='Sa'><img src='images/hubble_fork/tf_Sa.png'><span class='nl'>Sa</span></div>
            <div style='width:14px;height:1px;background:#22223a'></div>
            <div class='gnode' data-t='Sb'><img src='images/hubble_fork/tf_Sb.jpg'><span class='nl'>Sb</span></div>
            <div style='width:14px;height:1px;background:#22223a'></div>
            <div class='gnode' data-t='Sc'><img src='images/hubble_fork/tf_Sc.jpg'><span class='nl'>Sc</span></div>
        </div>
        <div class='arm-label' style='margin-top:8px;'>barred spirals</div>
        <div style='display:flex;align-items:center;gap:4px;'>
            <div class='gnode' data-t='SBa'><img src='images/hubble_fork/tf_SBa.jpg'><span class='nl'>SBa</span></div>
            <div style='width:14px;height:1px;background:#22223a'></div>
            <div class='gnode' data-t='SBb'><img src='images/hubble_fork/tf_SBb.jpg'><span class='nl'>SBb</span></div>
            <div style='width:14px;height:1px;background:#22223a'></div>
            <div class='gnode' data-t='SBc'><img src='images/hubble_fork/tf_SBc.jpg'><span class='nl'>SBc</span></div>
        </div>
        </div>
    </div>

    <div class='tf-panel empty' id='tfp'>
        <span class='hint'>Click a galaxy type above :)</span>
    </div>
    </div>

    <script>
    var D = {
    E0:  {name:'Elliptical E0',  tag:'ELLIPTICAL', tc:'#c8844a',
            desc:'Perfectly spherical. Old red stars, no star formation, no disc. These are common at the centres of galaxy clusters.',
            stats:[['Star formation',2],['Disc structure',0],['Bulge dominance',100],['Gas fraction',3]],
            sdss:'g−r ~ 0.85–0.95 &nbsp;|&nbsp; C ~ 3.0–3.5 &nbsp;|&nbsp; fracDeV ~ 1.0'},
    E3:  {name:'Elliptical E3',  tag:'ELLIPTICAL', tc:'#c8844a',
            desc:'Moderately flattened elliptical galaxy. Still featureless and red.',
            stats:[['Star formation',2],['Disc structure',5],['Bulge dominance',95],['Gas fraction',4]],
            sdss:'g−r ~ 0.82–0.92 &nbsp;|&nbsp; C ~ 2.8–3.3 &nbsp;|&nbsp; fracDeV ~ 0.9'},
    E7:  {name:'Elliptical E7',  tag:'ELLIPTICAL', tc:'#c8844a',
            desc:'Maximally flattened elliptical galaxy.',
            stats:[['Star formation',3],['Disc structure',15],['Bulge dominance',88],['Gas fraction',5]],
            sdss:'g−r ~ 0.78–0.90 &nbsp;|&nbsp; C ~ 2.5–3.2 &nbsp;|&nbsp; fracDeV ~ 0.8–1.0'},
    S0:  {name:'Lenticular S0',  tag:'LENTICULAR', tc:'#b08848',
            desc:'Has a disc like a spiral but no arms and no much star formation. It may be a quenched spiral that lost its gas through ram-pressure stripping or strangulation.',
            stats:[['Star formation',8],['Disc structure',70],['Bulge dominance',65],['Gas fraction',10]],
            sdss:'g−r ~ 0.65–0.85 &nbsp;|&nbsp; C ~ 2.5–3.0 &nbsp;|&nbsp; fracDeV ~ 0.5–0.9'},
    Sa:  {name:'Spiral Sa',      tag:'SPIRAL', tc:'#5577cc',
            desc:'Large bulge, tightly wound smooth arms. Star formation ongoing but modest.',
            stats:[['Star formation',40],['Disc structure',80],['Bulge dominance',55],['Gas fraction',22]],
            sdss:'g−r ~ 0.45–0.65 &nbsp;|&nbsp; C ~ 2.5–3.0 &nbsp;|&nbsp; fracDeV ~ 0.4–0.6'},
    Sb:  {name:'Spiral Sb',      tag:'SPIRAL', tc:'#5577cc',
            desc:'Intermediate bulge, moderate arms. Disc and bulge contribute roughly equally to total light.',
            stats:[['Star formation',62],['Disc structure',88],['Bulge dominance',38],['Gas fraction',32]],
            sdss:'g−r ~ 0.35–0.55 &nbsp;|&nbsp; C ~ 2.2–2.8 &nbsp;|&nbsp; fracDeV ~ 0.2–0.4'},
    Sc:  {name:'Spiral Sc',      tag:'SPIRAL', tc:'#5577cc',
            desc:'Tiny bulge, loosely wound patchy arms full of young blue stars. Highest star formation of all spiral types.',
            stats:[['Star formation',88],['Disc structure',97],['Bulge dominance',10],['Gas fraction',50]],
            sdss:'g−r ~ 0.20–0.42 &nbsp;|&nbsp; C ~ 1.8–2.3 &nbsp;|&nbsp; fracDeV ~ 0.0–0.1'},
    SBa: {name:'Barred Spiral SBa', tag:'BARRED SPIRAL', tc:'#4488bb',
            desc:'Prominent bar with tightly wound arms from its ends.',
            stats:[['Star formation',38],['Disc structure',82],['Bulge dominance',52],['Gas fraction',24]],
            sdss:'g−r ~ 0.45–0.65 &nbsp;|&nbsp; C ~ 2.4–3.0 &nbsp;|&nbsp; fracDeV ~ 0.4–0.6'},
    SBb: {name:'Barred Spiral SBb', tag:'BARRED SPIRAL', tc:'#4488bb',
            desc:'Intermediate barred spiral. Moderate bulge, strong bar, moderately wound arms.',
            stats:[['Star formation',60],['Disc structure',90],['Bulge dominance',35],['Gas fraction',34]],
            sdss:'g−r ~ 0.33–0.52 &nbsp;|&nbsp; C ~ 2.1–2.7 &nbsp;|&nbsp; fracDeV ~ 0.2–0.4'},
    SBc: {name:'Barred Spiral SBc', tag:'BARRED SPIRAL', tc:'#4488bb',
            desc:'Small bulge, strong bar, loosely wound arms. Maximum star formation rate.',
            stats:[['Star formation',92],['Disc structure',97],['Bulge dominance',8],['Gas fraction',52]],
            sdss:'g−r ~ 0.18–0.40 &nbsp;|&nbsp; C ~ 1.8–2.2 &nbsp;|&nbsp; fracDeV ~ 0.0–0.1'}
    };
    var SC={'Star formation':'#74c7ec','Disc structure':'#6688ee','Bulge dominance':'#f38ba8','Gas fraction':'#69db7c'};
    var active=null;
    document.querySelectorAll('.gnode').forEach(function(n){
    n.addEventListener('click',function(){
        if(active)active.classList.remove('active');
        n.classList.add('active');active=n;
        var d=D[n.dataset.t],p=document.getElementById('tfp');
        p.classList.remove('empty');
        p.innerHTML='<div><div class="tf-name">'+d.name+'</div>'
        +'<span class="tf-tag" style="background:'+d.tc+'22;color:'+d.tc+';border:1px solid '+d.tc+'44">'+d.tag+'</span>'
        +'<div class="tf-desc">'+d.desc+'</div>'
        +'<div class="tf-sdss">SDSS: '+d.sdss+'</div></div>'
        +'<div class="tf-stats">'+d.stats.map(function(s){
            return '<div class="srow"><span class="slabel">'+s[0]+'</span>'
            +'<div class="strack"><div class="sbar" style="width:0%;background:'+(SC[s[0]]||'#8888aa')+'"></div></div></div>';
        }).join('')+'</div>';
        requestAnimationFrame(function(){
        p.querySelectorAll('.sbar').forEach(function(b,i){b.style.width=d.stats[i][1]+'%';});
        });
    });
    });
    document.querySelector('[data-t="Sb"]').click();
    </script>"""
    
    return out
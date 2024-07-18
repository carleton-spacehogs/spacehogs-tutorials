'''
Usage: Python3 timelineCreator.py [relation csv] [ecceTera output path] [file output name]

Documentation can be found on the carleton-spacehogs github page.
Created for Spacehogs Lab by Will Puzella
Summer 2024
'''




import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import csv
import sys
import glob

def generate_unique_colors(n, colormap='tab20'):
    """
    Generate a list of unique colors in hexadecimal format.

    Parameters:
    - n: int, the number of unique colors needed.
    - colormap: str, the name of the colormap to use.

    Returns:
    - colors: list of hex color codes.
    """
    cmap = plt.get_cmap(colormap)
    colors = [mcolors.to_hex(cmap(i / n)) for i in range(n)]
    return colors

def add_jitter_y(arr, scale=0.2):
    return arr + np.random.normal(scale=scale, size=arr.shape)

# Data for the example

masterDataFile = sys.argv[1]
dataPath = sys.argv[2]
masterData = csv.DictReader(open(masterDataFile,mode="r", encoding="utf-8-sig"), delimiter=",")
genes = []
geneIDs = []
geneFunctions = []
annotations = []



# check that all the genes have appropriate info
for geneInfo in masterData:
    fileName = geneInfo["Gene ID"] + "_symmetric.events_event_dates.txt"
    if len(glob.glob(dataPath + fileName)) == 0:
        print(geneInfo["Gene ID"] + " does not exist in pipeline output removing from final gene list")
        
    else:
        if len(geneInfo.keys()) == 4:
            annotations.append(geneInfo["Annotation"])
        genes.append(geneInfo["Gene Name"])
        geneIDs.append(geneInfo["Gene ID"])
        geneFunctions.append(geneInfo["Function"])

num_genes = len(genes)

# Removes only unique values for function labels
list_set = set(geneFunctions)
functions = (list(list_set))

# Colors for each function
function_colors = generate_unique_colors(len(functions))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(16, 14))

# Data for gene events
gene_events = ["dup", "hgt", "los", "spe"]
event_markers = {"dup": 's', "hgt": 'o', "los": '^', "spe": '*'}

# Plot the data with different markers for each gene event
for i, gene in enumerate(genes):
    print("Current gene: " + gene)
    geneDataFile = csv.DictReader(open(dataPath + geneIDs[i] +"_symmetric.events_event_dates.txt"), delimiter="\t")
    for line in geneDataFile:
        if line["right node"] != "UNSAMPLED":
            if line["event"] == "spe":
                x = float(line["right date"])
            else:
                x = float(line["midpoint date"])
            y = np.array([i])
            y_jittered = add_jitter_y(y, scale=0.1)
            ax.scatter(x, y_jittered, label=f'{genes[i]}-{geneFunctions[i]}-{line["event"]}', color=function_colors[functions.index(geneFunctions[i])], alpha=0.7, marker=event_markers.get(line["event"]))

# Customizing the plot
ax.set_yticks(range(num_genes))
ax.set_yticklabels(genes)
ax.set_xticks(range(0, 4501, 500))
ax.set_xlabel('Million Years Ago')
ax.set_ylabel('Gene')
ax.grid(True)

# Adding the GOE shading
ax.axvspan(2500, 2300, color='grey', alpha=0.3, label='GOE')

# Adding geological periods as small boxes with alternating colors
periods = [
    ("MesoArc.", 3200, 2800),
    ("NeoArc.", 2800, 2500),
    ("PaleoPtz.", 2300, 1600),
    ("MesoPtz.", 1600, 1000),
    ("NeoPtz.", 1000, 550),
    ("Phan.", 550, 0)
]
colors = ["lightgrey", "darkgrey"]
for idx, (period, start, end) in enumerate(periods):
    rect = patches.Rectangle((start, -1.5), end - start, 0.5, linewidth=1, edgecolor='black', facecolor=colors[idx % 2], alpha=0.5)
    ax.add_patch(rect)
    ax.text((start + end) / 2, -1.25, period, ha='center', va='center', fontsize=10)

# Addition of Annotations
if len(annotations) != 0:
    print("Annotations found")
    for i, reaction in enumerate(annotations):
        ax.text(-200, i, reaction, ha='left', va='center', fontsize=10, color='black')


# Legend for functions
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=fc, markersize=10) for fc in function_colors]
labels = functions
legend1 = ax.legend(handles, labels, title="Metabolic Cycle", loc='upper left')

# Legend for gene events
event_handles = [plt.Line2D([0], [0], marker=event_markers[event], color='w', markerfacecolor='black', markersize=10) for event in gene_events]
event_labels = gene_events
legend2 = ax.legend(event_handles, event_labels, title="Gene Event", loc='upper right')
ax.add_artist(legend1)  # Add the first legend back

# Adjust the plot limits to fit the geological period labels
ax.set_ylim(-2, num_genes)

# Show the plot
plt.gca().invert_xaxis()
plt.tight_layout()
plt.savefig(sys.argv[3])

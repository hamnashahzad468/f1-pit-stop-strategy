import fastf1
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# Create cache folder
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')

# Load 2026 Austrian GP
session = fastf1.get_session(2026, 'Austria', 'R')
session.load()

# Top 5 finishers
drivers = ['RUS', 'VER', 'ANT', 'PIA', 'HAM']

# Tyre compound colours
compound_colours = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFF200',
    'HARD': '#DDDDDD',
    'INTERMEDIATE': '#39B54A',
    'WET': '#0067FF',
    'UNKNOWN': '#AAAAAA'
}

fig, ax = plt.subplots(figsize=(14, 7))

for i, driver in enumerate(drivers):
    laps = session.laps.pick_driver(driver).copy()
    
    # Fill missing compound data forward
    laps['Compound'] = laps['Compound'].fillna('UNKNOWN')
    
    for _, lap in laps.iterrows():
        compound = lap['Compound'] if lap['Compound'] in compound_colours else 'UNKNOWN'
        colour = compound_colours[compound]
        ax.barh(
            y=i,
            width=1,
            left=lap['LapNumber'] - 1,
            color=colour,
            edgecolor='none',
            height=0.6
        )

# Axis formatting
ax.set_yticks(range(len(drivers)))
ax.set_yticklabels(drivers, fontsize=12, fontweight='bold')
ax.set_xlabel('Lap Number', fontsize=12)
ax.set_title('Pit Stop Strategy Comparison — Austrian GP 2026', fontsize=14, fontweight='bold')
ax.set_xlim(0, 71)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# Legend
legend_patches = [
    mpatches.Patch(color='#FF3333', label='Soft'),
    mpatches.Patch(color='#FFF200', label='Medium'),
    mpatches.Patch(color='#DDDDDD', label='Hard'),
    mpatches.Patch(color='#39B54A', label='Intermediate'),
    mpatches.Patch(color='#0067FF', label='Wet'),
    mpatches.Patch(color='#AAAAAA', label='Unknown'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('pit_stop_strategy.png', dpi=150, bbox_inches='tight')
plt.show()

print("Done! Chart saved as pit_stop_strategy.png")

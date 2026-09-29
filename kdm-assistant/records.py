"""Reviewed summaries of the supplied 1.5 scan. Original PDF pages are identifiers."""
from core_records import CORE_RECORDS

RECORDS = [
    {
        "id": "hands-of-heat", "title": "Hands of Heat", "original": 129,
        "keywords": "experiment lanterns lantern branding lantern oven red fist bone witch courage",
        "layout": "Three regions: left entry condition and event; center Experiment with Lanterns; right Lantern Branding. Diamond numerals label center outcomes; right table uses printed ranges.",
        "summary": "If the settlement already has Lantern Oven, skip the experiment and use Lantern Branding. Otherwise nominate a survivor, grant +1 courage, and roll 1d10 on Experiment with Lanterns.",
        "notes": ["Lantern Branding costs half the settlement's total resources, including storage, rounded down; nominate a survivor and roll 1d10.", "Only the experiment's 7+ outcome directs a further Lantern Branding roll. A 4-6 outcome does not.", "Do not reuse an experiment roll as the new branding roll."],
        "tables": [
            {"id": "experiment", "title": "Experiment with Lanterns", "die": "1d10", "crop": [0.345, 0.29, 0.605, 0.93], "rows": [
                {"min": 1, "max": 3, "label": "1-3", "effects": ["The nominated survivor is exiled; settlement loses 1 population.", "Settlement gains Lantern Oven.", "Add Bone Witch to the timeline 3 lantern years from now."]},
                {"min": 4, "max": 6, "label": "4-6", "effects": ["Nominated survivor gains +1 permanent strength.", "Nominated survivor gains the Red Fist secret fighting art.", "Settlement gains the Lantern Oven innovation."]},
                {"min": 7, "max": None, "label": "7+", "effects": ["Settlement gains Lantern Oven.", "Nominated survivor gains the Red Fist secret fighting art.", "Proceed to Lantern Branding and make its separate roll."], "next_table": "branding"},
            ]},
            {"id": "branding", "title": "Lantern Branding", "die": "1d10", "crop": [0.61, 0.53, 0.87, 0.925], "rows": [
                {"min": 1, "max": 3, "label": "1-3", "effects": ["All departing survivors gain +10 survival.", "Add Hands of Heat to the timeline 1d10 years from now."]},
                {"min": 4, "max": 7, "label": "4-7", "effects": ["Nominated survivor gains +1 permanent speed (branded feet)."]},
                {"min": 8, "max": 9, "label": "8-9", "effects": ["Nominated survivor gains +1 permanent strength (branded hand)."]},
                {"min": 10, "max": None, "label": "10+", "effects": ["Nominated survivor suffers the blind severe head injury and gains +1 permanent luck."]},
            ]},
        ],
    },
    {
        "id": "affinities", "title": "Affinities", "original": 51,
        "keywords": "affinity puzzle lucky charm fecal salve hunter whip blue red green gear bonus lost",
        "layout": "Three columns with gear-grid diagrams. Normal square requirements count completed affinities anywhere; puzzle symbols require completion at the pictured edge of that specific card.",
        "summary": "Adjacent half-squares of the same color form one affinity. Ordinary affinity requirements count completed affinities on the survivor's gear grid. Puzzle affinity requirements must be completed at the indicated edges of that specific gear card.",
        "notes": ["Lucky Charm needs two blue affinities for its +1 luck bonus.", "Each piece of gear grants its affinity bonus once. Five blue affinities still give only +1 luck from Lucky Charm.", "An additional identical piece of gear cannot grant a second affinity bonus.", "If gear is lost and the requirements are no longer completed, dependent affinity bonuses are lost."],
        "tables": [],
    },
    {
        "id": "critical-wound-examples", "title": "Critical wound examples", "original": 81,
        "keywords": "critical wounds lantern 10 luck reflex furious gut fleshy gut restless rump wound reaction",
        "layout": "Three independent photo/caption panels. Green checks demonstrate critical wounds; the orange X rejects a critical-wound interpretation of a lantern 10 on a location without a critical effect.",
        "summary": "These examples distinguish a successful wound from a critical wound. The hit location's critical-wound effect matters, and luck can make a lower die result critical.",
        "notes": ["Fleshy Gut: Allister rolls a lantern 10, wounds, gains +3 insanity and a random basic resource from the critical effect.", "Furious Gut: Erza rolls a lantern 10. This location has no critical-wound effect, so the result is a normal wound and its wound reaction is performed.", "Restless Rump: Lucy has two +1 luck tokens and rolls 8, causing a critical wound. The Reflex reaction that would knock down Erza is canceled; the critical effect is performed instead."],
        "tables": [],
    },
    {
        "id": "create-survivor", "title": "Create a Survivor", "original": 28,
        "keywords": "starting gear cloth founding stone name survival dodge movement speed accuracy survivor record",
        "layout": "Top photo labels gear grid and record sheet. Lower text reads down each of three columns; survival explanation continues into the right column.",
        "summary": "In the First Story setup, each survivor starts with one Cloth armor gear card and one Founding Stone weapon gear card. Put them in any two gear-grid spaces. Naming the survivor grants +1 survival.",
        "notes": ["The survivor record sheet tracks the survivor's life and changing attributes.", "Only dodge is available in the First Story; dash, encourage, and surge are gained as play develops.", "Spending survival reduces the recorded total. Survival does not replenish at the end of each showdown.", "Starting attributes shown here: movement 5, speed 0, accuracy 0. Speed is attack rate; accuracy is attack precision.", "The attribute explanation continues on the following book page; this record is limited to printed page 24."], "tables": [],
    },
    {
        "id": "white-lion-setup", "title": "First Story: White Lion", "original": 30,
        "keywords": "prologue showdown setup ai deck claw chomp size up power swat grasp maul terrifying roar enraged strange hand six spaces",
        "layout": "Numbered instructions connect to blue numbered markers in a board diagram. AI deck list has Basic, Advanced, and Legendary groupings. Card-back images distinguish AI, hit location, and resource cards.",
        "summary": "The First Story uses a predetermined White Lion AI deck. Basic: Claw, Chomp, Size Up, Power Swat, Grasp. Advanced: Maul, Terrifying Roar, Enraged. No Legendary cards.",
        "notes": ["Set Claw aside, shuffle the rest face down, then place Claw face down on top.", "Set Strange Hand aside from hit locations, shuffle the rest face down, then place Strange Hand face down on top.", "Place the double-sided Basic Action / Monster Reference card on the monster control panel.", "Arrange survivor records and gear grids around the showdown board.", "Place the White Lion in the board center. Place each survivor 6 spaces away, counting cardinally, not diagonally, on the blue diagram spaces."], "tables": [],
    },
] + CORE_RECORDS

"""Scoped rule summaries checked against the rendered edition 1.5 source pages.

Original PDF identifiers are stable; supporting_originals preserve continuations.
Community questions are evaluation prompts, never rule authorities.
"""

CORE_RECORDS = [
    {
        'id': 'white-lion-deployment', 'title': 'White Lion: standard showdown deployment', 'original': 183,
        'keywords': 'white lion showdown setup start starting blue zone squares enclosed area placement deployment level 1',
        'layout': 'The showdown diagram has a blue outline of individual survivor spaces and one red monster marker. The legend identifies colored spaces. The terrain instructions below it refer back to this diagram. This is the standard showdown story event, separate from First Story setup.',
        'summary': 'For the standard White Lion showdown, place survivors on the blue marked squares in the setup diagram. The uncolored interior of the blue outline is not marked as survivor deployment space. This reading combines the diagram, its legend, and the instruction to place survivors in the blue zone.',
        'notes': ['Place the White Lion in the center of the board.', 'Use 1 Tall Grass terrain card, which supplies 2 Tall Grass tiles, and 2 random terrain cards set up normally.', 'This record covers deployment only. Use First Story: White Lion for the prologue setup; the standard showdown page also contains level and aftermath rules outside this record.'],
        'tables': [],
    },
    {
        'id': 'survival-actions', 'title': 'Survival actions and timing', 'original': 82, 'supporting_originals': [83],
        'keywords': 'survival actions surge dash dodge encourage endure attacking attacker fellow survivor before after movement activation tall grass hide timing opportunity opportunities interrupt',
        'layout': 'Printed page 78 has three columns: action definitions, survival opportunities, then limitations and examples. Its monster-flow example continues at the top left of printed page 79. The During Survivor Attacks heading on page 79 defines two separate interrupt windows.',
        'summary': 'Surge spends 1 survival to gain an activation that must be used immediately. Dash spends 1 survival to gain movement that must be used immediately. During the survivors\' turn, survival opportunities occur before or after completed movement or activation. A survivor who is attacking cannot perform survival actions, including dodge.',
        'notes': [
            'The book example has Erza complete movement next to the monster. Zachary, already near Tall Grass, then surges and uses the activation to hide. Erza resumes her act and activates her weapon. The example does not use Surge to grant movement.',
            'During another survivor\'s attack, a fellow survivor has an opportunity after the wound roll but before the monster\'s reaction; if the hit location has no reaction, this window is absent. A second window occurs after critical wound effects are applied and before the hit-location card is discarded.',
            'Resolve a survival action and all its consequences before resuming the interrupted turn or attack. No new survival action can begin while a current survival action remains unresolved.',
            'Monster AI flows, including flows on Basic Action, provide opportunities. Outside a flow on the monster turn, a survival action opportunity exists when the monster is knocked down.',
            'Dodge costs 1 survival and cancels one monster hit, chosen after hit locations are rolled and before severe injury rolls. Other undodged hits resolve normally. Knocked-down survivors can dodge; dodge is their only available survival action.',
            'A survivor may perform each survival action once per round. The campaign starts with dodge; the other survival actions are learned from innovations. Being an attacker and being doomed are distinct restrictions.',
            'Encourage costs 1 survival and requires a standing survivor; it lets another knocked-down survivor stand. Endure costs 7 survival minus Luck to ignore a severe injury before rolling its result. Their stated timing rules still apply.',
        ], 'tables': [],
    },
    {
        'id': 'monster-hit-damage', 'title': 'Monster hits, damage, and injury order', 'original': 74,
        'related_ids': ['survival-actions', 'attack-effects'],
        'keywords': 'monster attack speed damage hits hit locations armor armour light heavy severe injury injuries dodge two both multiple same location',
        'layout': 'The left column defines the attack profile and Speed, the center continues with Accuracy, Damage, and hit locations, and the right column gives damage order. The damage arrow diagram illustrates the same sequence as the numbered text. Opening text about movement continues from the previous page and is outside this record.',
        'summary': 'A monster rolls attack dice equal to its attack speed and rolls one hit-location die for each successful hit. Damage is the amount dealt by each hit. Resolve hits separately, one at a time, in the target\'s chosen order, even if several hits land on the same location.',
        'notes': [
            'Speed and damage include the applicable monster attributes and tokens. An attack roll plus monster accuracy modifier must meet or exceed attack-profile accuracy plus survivor evasion.',
            'For one hit, spend damage at its single location: reduce armor to zero first, then fill light and heavy injury boxes in that order. Filling the heavy box knocks the survivor down.',
            'If damage remains after armor and the available injury boxes are exhausted, expend all remaining damage from that hit on one severe injury roll for that location. Another hit to the same location is a separate instance and can cause another severe injury.',
            'Worked application: a Speed 2, Damage 3 attack with two successful hits has two hits worth 3 damage each, before applicable modifiers. If the survivor is allowed to dodge and dodges one, the remaining hit deals 3 damage to its rolled location. The final injury depends on that location\'s current armor and checked boxes.',
            'Dodge eligibility and timing are on the linked Survival actions pages. Attack triggers such as After Hit and After Damage have their own timing on the linked Attack effects page.',
        ], 'tables': [],
    },
    {
        'id': 'attack-effects', 'title': 'Attack effects and damage outside attacks', 'original': 75,
        'related_ids': ['monster-hit-damage', 'survival-actions'],
        'keywords': 'trigger after hit before damage after damage dodge grab intimidate brain damage insanity bash bleed knockback',
        'layout': 'The left column lists attack triggers and common effects. Intimidate continues into the center column, followed by Brain Damage. Damage Outside of Attack Actions is a separate right-column heading. Duration and survivor-status AI sections are outside this record.',
        'summary': 'Attack-profile effects trigger once per attack at their specified step. Damage outside an attack profile cannot be dodged because it does not come from a hit.',
        'notes': [
            'After Hit: if there are successful hits, apply the effect before rolling hit-location dice. Before Damage: apply after attack and location rolls, before damage. After Damage: resolve all hits\' damage first; apply the effect if the attack dealt damage.',
            'Bash knocks the survivor down. Bleed X grants X bleeding tokens, or 1 if no number is specified. Knockback X pushes the target X spaces in the stated direction; the monster controller chooses the direction when none is stated.',
            'Intimidate actions are not attacks, cause brain damage instead of physical-location damage, and cannot be dodged. Follow the action\'s specific rules.',
            'Brain damage uses insanity as armor, then the brain injury box, then Brain Trauma rolls. It is distinct from physical head damage.',
            'Damage outside attack profiles is resolved normally but is not modified by monster attributes or tokens. If no location is specified, roll a hit-location die. The book gives White Lion Grab as an example of additional damage.',
        ], 'tables': [],
    },
    {
        'id': 'moods-and-flows', 'title': 'AI flows, moods, and Ground Fighting', 'original': 71, 'supporting_originals': [70],
        'related_ids': ['priority-target'],
        'keywords': 'white lion ground fighting groundfighting mood moods trait ai flow draw card basic action zone death activation priority',
        'layout': 'Printed page 66 shows Combo Claw with action and flow labels. Page 67 continues that example through the left and center columns; the right column has a separate Playing Moods & Traits section with a pictured Ground Fighting card and explanatory paragraph.',
        'summary': 'Moods and traits have persistent effects while their cards remain in play. Apply their conditional actions when triggered. The book\'s Ground Fighting example stops normal AI draws, monitors the pictured Zone of Death for survivors spending activation, and is discarded when the White Lion is wounded.',
        'notes': [
            'Normally a monster turn has Start Turn, Draw AI, and End Turn. Read the full AI card, then complete its actions in order. If instructed to draw another AI card, finish applicable actions on the current card first.',
            'Flows between AI actions create survival opportunities for eligible survivors. Finish survival actions before continuing the next monster action.',
            'Ground Fighting instructs a Basic Action targeting a survivor who spends activation in its Zone of Death before resolving that activation, with +2 speed and +1 damage for that attack. Its pictured zone must be consulted. It stops drawing AI cards while in play.',
            'After Ground Fighting is discarded by a wound, the book says the White Lion\'s behavior returns to normal.',
            'For an interaction involving a permanent priority target, also read the Priority targeting record and its linked Fuzzy Groin card source.',
        ], 'tables': [],
    },
    {
        'id': 'priority-target', 'title': 'Priority targeting and its exceptions', 'original': 72, 'supporting_originals': [73],
        'card_sources': [{'title': 'Fuzzy Groin (White Lion hit location)', 'url': 'https://kingdomdeath.fandom.com/wiki/Fuzzy_Groin', 'edition': '1.5', 'provenance': 'community card transcription'}],
        'keywords': 'priority target token targeting permanent fuzzy groin ground fighting groundfighting pick target exceptions reaction',
        'layout': 'Printed page 68 puts Priority Target Token at the bottom of the right column. Its restrictions continue at the top left of printed page 69, before Move & Attack Target Actions. Those continuation paragraphs belong to priority targeting.',
        'summary': 'The priority-target token overrides other targeting conditions when a monster performs a Pick Target action on an AI or special card. It does not replace every form of targeting or create an instruction to draw AI or move.',
        'notes': [
            'Only one survivor holds the priority-target token at a time. Under the ordinary token rule, the survivor discards it when picked as the target.',
            'The continuation excludes AI cards targeting multiple or all survivors, monster-AI targeting outside a Pick Target action, and hit-location targeting. A reaction that targets the attacker is unaffected by the token.',
            'The continuation is printed page 69 (original PDF 73). The main Pick Target and token rules are printed page 68 (original PDF 72).',
            'Fuzzy Groin critical wound gives the attacker a permanent priority-target token and directs the White Lion to attack that survivor until one of them dies. It also grants the monster +1 damage token. The ordinary token discard rule does not end this card-specific persistent effect.',
        ], 'tables': [],
    },
    {
        'id': 'survivor-attack-sequence', 'title': 'Survivor acts and attack sequence', 'original': 77, 'supporting_originals': [78],
        'related_ids': ['survival-actions'],
        'keywords': 'survivor act attack activation movement move adjacent melee reach ranged range wound steps reaction first strike before after',
        'layout': 'Printed page 73 separates Survivors\' Turn and Act Overview from Movement, Activation, and How Survivors Attack. Printed page 74 has the attack sequence in the left column and a shaded wound-steps panel across the middle and right columns. Read that panel down the middle and then down the right.',
        'summary': 'A survivor\'s act grants one movement and one activation. They can be spent in either order, completing one action before another begins. An attack begins by activating a weapon; completing movement next to a monster is distinct from making that attack.',
        'notes': [
            'Survivors act one at a time in any chosen order and lose unspent movement and activation at the end of their act. Specific survival opportunities allow interruptions, as covered by the linked survival rules.',
            'Normal movement uses cardinal steps into adjacent unoccupied spaces. Survivors cannot move through monsters or other survivors, including knocked-down models.',
            'Melee weapons require adjacency unless they have reach. Ranged weapons use their range and cannot attack through blocked field of view; Obstacle terrain blocks field of view.',
            'For an attack, roll dice equal to weapon speed plus survivor speed modifier, determine hits using accuracy and monster evasion, then draw a hit location for each hit. Read all hit locations. A drawn Trap ends the attack(s) and is resolved immediately.',
            'Resolve First Strike locations first. For each location: perform its special rules, attempt a wound, check critical wounds, wound the monster when applicable, allow eligible fellow-survivor reactions, perform applicable monster reactions, and discard the resolved location. Continue for unresolved locations.',
            'Wound reactions apply on success, Failure on failure, and Reflex normally always applies unless canceled by a critical wound. The precise survival windows and restrictions are on the linked survival pages.',
        ], 'tables': [],
    },
]

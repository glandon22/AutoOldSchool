import osrs.queryHelper
import util_functions
import transport_functions

dialogue = [
    "Sure thing."
]

response = [
    "Sunlight",
    "The Slayer Masters",
    "Three",
    "Squamata",
    "It becomes sleepy",
    "Hair",
    "Mibbiwocket",
    "Vegetables",
    "Admiral Bake",
    "Hard shell",
    "Twenty years",
    "Gnomes",
    "Runite",
    "Anti-dragon-breath shield",
    "Unknown",
    "Elemental",
    "Old battle sites",
    "Twelve",
    "Climate change",
    "Two",
    "Asgarnia",
    "Reptiles",
    "Dragons",
    "Below room temperature",
    "It is resistant to acid",
    "Spitting acid",
    "Fireproof oil",
    "Acid-spitting snail",
    "Contracting and stretching",
    "An operculum",
    "Stomach acid",
    "Tongue",
    "Seeing how you smell",
    "Constriction",
    "Squamata",
    "Anywhere",
    "Nematocysts",
    "The researchers keep vanishing",
    "Seaweed",
    "Defence or display",
    "Ardougne",
    "They have a hard shell",
    "Simian",
    "Harmless",
    "Bitternuts",
    "Harmless",
    "Red",
    "Seaweed",
    "Pasha",
    "Worker",
    "Lamellae",
    "Carnivores",
    "Scarab beetles",
    "Scabaras",
    "Anything",
    "Gnomes",
    "Eating plants",
    "Four",
    "Stones",
    "0",
    "Sight",
    "Planning",
    "A layer of fat",
    "Cold",
    "Social",
    "During breeding",
    "Subterranean",
    "They dig holes",
    "Wyson the Gardener",
    "A labour",
    "Insects and other invertebrates",
    "The Talpidae family",
    "Toxic dung",
    "Two",
    "Omnivore",
    "Annoyed",
    "Al Kharid",
    "Milk",
    "Water",
    "'Y'-shaped",
    "Apples",
    "Environment",
    "They attack by jumping",
    "It doubles in size",
]

plaques = [
    [24609, 24610, 24611, 24612],
    [24605, 24606, 24607, 24608],
    [24613, 24614, 24615, 24616],
    [24617, 24618],
]

main_quiz_holder = '533,27'
opt1 = '533,29'
opt2 = '533,30'
opt3 = '533,31'
dialogue_snippet = '231,6'


def quiz_handler(i):
    for plaque in plaques[i]:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_objects_v2('game', {plaque})
        qh.set_widgets({main_quiz_holder, opt1, opt2, opt3, util_functions.main_chat_widget, dialogue_snippet})
        while True:
            qh.query_backend()
            if qh.get_widgets(dialogue_snippet) and 'Bonza' in qh.get_widgets(dialogue_snippet)['text']:
                osrs.keeb.press_key('space')
                osrs.clock.random_sleep(1, 1.1)
                break

            if qh.get_widgets(util_functions.main_chat_widget):
                osrs.keeb.press_key('space')
                osrs.clock.random_sleep(1, 1.1)
            elif not qh.get_widgets(main_quiz_holder) and qh.get_objects_v2('game', plaque):
                osrs.move.click(qh.get_objects_v2('game', plaque)[0])
            elif qh.get_widgets(main_quiz_holder):
                for opt in [opt1, opt2, opt3]:
                    if qh.get_widgets(opt) and 'col=00f88' in qh.get_widgets(opt)['text']:
                        osrs.move.click(qh.get_widgets(opt))
                        osrs.clock.sleep_one_tick()



def main():
    util_functions.talk_to_npc('orlando smith')
    util_functions.dialogue_handler(dialogue)
    transport_functions.walk_to_loc(1741, 1743, 4959, 4962, 1742, 4960)
    quiz_handler(0)
    transport_functions.walk_to_loc(1760, 1762, 4976, 4978, 1761, 4977)
    quiz_handler(1)
    transport_functions.walk_to_loc(1772, 1774, 4956, 4960, 1773, 4948)
    quiz_handler(2)
    transport_functions.walk_to_loc(1757, 1759, 4944, 4946, 1758, 4945)
    quiz_handler(3)
    transport_functions.walk_to_loc(1757, 1759, 4950, 4952, 1758, 4951)
    util_functions.talk_to_npc('orlando smith')
    util_functions.dialogue_handler(dialogue)
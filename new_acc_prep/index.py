import random

import cooks_assistant
import transport_functions
import util_functions
import sheep_shearer_v2
import imp_catcher
import osrs
import witchs_potion
from prayer import gilded_v2
from firemaking import burn_logs_varrock
import romeo_and_juliet
import vampire_slayer
import dorics_quest
import goblin_diplomacy
import witchs_house
import druidic_ritual
import rune_mysteries
import natural_history_quiz
import waterfall_quest
from agility import gnome_v2
import grand_tree
import tree_gnome_village
import monks_friend
import plague_city
import sea_slug
import knights_sword
import fight_arena
from thieving import steal_tea_and_make_arrow_shafts
from crafting import blow_glass_v3
from herblore import make_pots_v2
from combat import early_acc_cow_killer
from rc import airs_v2
from cooking import rogues_den_cooker
from construction import wooden_chairs_v2, plant_dead_trees
from construction.utils import build_study, build_oak_lectern

'''
cooks_assistant.main()
transport_functions.bank_in_lumby()
util_functions.get_quest_items([
    {
        'id': [
            osrs.item_ids.ItemIDs.BALL_OF_WOOL.value
        ],
        'quantity': 'All'
    },
    osrs.item_ids.ItemIDs.AMULET_OF_GLORY6.value,
    {
        'id': osrs.item_ids.ItemIDs.COINS_995.value,
        'quantity': 'X',
        'amount': '100k'
    },
    osrs.item_ids.ItemIDs.RED_BEAD.value,
    osrs.item_ids.ItemIDs.YELLOW_BEAD.value,
    osrs.item_ids.ItemIDs.WHITE_BEAD.value,
    osrs.item_ids.ItemIDs.BLACK_BEAD.value,
])
transport_functions.bank_to_lumby_ground()
transport_functions.walk_to_sheep_shearer()
sheep_shearer_v2.main()
transport_functions.leave_farmer_freds_house()
transport_functions.walk_to_wizards_tower()
imp_catcher.main()
transport_functions.glory_to_draynor()
util_functions.get_quest_items([
    {
        'id': [
            osrs.item_ids.ItemIDs.DRAGON_BONES.value
        ],
        'quantity': 'All',
        'noted': True
    },
    osrs.item_ids.ItemIDs.IRON_SCIMITAR.value,
    {
        'id': osrs.item_ids.ItemIDs.COINS_995.value,
        'quantity': 'X',
        'amount': '100k'
    },
    osrs.item_ids.ItemIDs.EYE_OF_NEWT.value,
    osrs.item_ids.ItemIDs.BURNT_MEAT.value,
    osrs.item_ids.ItemIDs.ONION.value
])
osrs.move.go_to_loc(2959, 3209)
witchs_potion.main()
transport_functions.leave_hettys_house()
util_functions.hop_to(330)
gilded_v2.main()
util_functions.hop_to(337)
osrs.move.go_to_loc(3095, 3248)
util_functions.get_quest_items([
    osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
    osrs.item_ids.ItemIDs.GARLIC.value,
    osrs.item_ids.ItemIDs.HAMMER.value,
    osrs.item_ids.ItemIDs.CADAVA_BERRIES.value,
    osrs.item_ids.ItemIDs.BEER.value,
    {
        'id': osrs.item_ids.ItemIDs.MIND_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY6.value,
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY5.value,
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY4.value,
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY3.value,
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY2.value,
            osrs.item_ids.ItemIDs.AMULET_OF_GLORY1.value,
        ],
        'quantity': '1'
    },
])
util_functions.equip_air_staff_and_earth_strike()
osrs.move.go_to_loc(3092,3271)
vampire_slayer.main()
util_functions.tab_to_varrock()
romeo_and_juliet.main()
transport_functions.walk_to_ge()
util_functions.get_quest_items([])
osrs.bank.ge_handler([
    {'id': osrs.item_ids.ItemIDs.GOBLIN_MAIL.value, 'quantity': 3},
    {'id': osrs.item_ids.ItemIDs.BLUE_DYE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.ORANGE_DYE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.CLAY.value, 'quantity': 6},
    {'id': osrs.item_ids.ItemIDs.IRON_ORE.value, 'quantity': 2},
    {'id': osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value, 'quantity': 10},
    {'id': osrs.item_ids.ItemIDs.COPPER_ORE.value, 'quantity': 4},
])
util_functions.get_quest_items([
    {
        'id': osrs.item_ids.ItemIDs.GOBLIN_MAIL.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.CLAY.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.IRON_ORE.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.COPPER_ORE.value,
        'quantity': 'All'
    },
    osrs.item_ids.ItemIDs.BLUE_DYE.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    osrs.item_ids.ItemIDs.ORANGE_DYE.value,
])
transport_functions.tab_to_fally()
dorics_quest.main()
transport_functions.leave_dorics()
transport_functions.walk_to_loc(2947, 2962, 3500, 3510, 2956, 3503)
goblin_diplomacy.main()
util_functions.tab_to_varrock()
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id_override': 'prayer potion(4)', 'quantity': 3},
    {'id': osrs.item_ids.ItemIDs.CHEESE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.RAW_CHICKEN.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.RAW_BEEF.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.RAW_RAT_MEAT.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.RAW_BEAR_MEAT.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.LEATHER_GLOVES.value, 'quantity': 1},
])
quest_items = [
    {
        'id': osrs.item_ids.ItemIDs.MIND_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
        'quantity': 'All'
    },
    osrs.item_ids.ItemIDs.CHEESE.value,
    osrs.item_ids.ItemIDs.LEATHER_GLOVES.value,
    osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value,
    osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
    osrs.item_ids.ItemIDs.RAW_CHICKEN.value,
    osrs.item_ids.ItemIDs.RAW_BEEF.value,
    osrs.item_ids.ItemIDs.RAW_RAT_MEAT.value,
    osrs.item_ids.ItemIDs.RAW_BEAR_MEAT.value,
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
transport_functions.tab_to_fally()
transport_functions.walk_to_loc(2940, 2948, 3449, 3454, 2948, 3451)
transport_functions.fally_to_tav_gate()
witchs_house.main()
transport_functions.walk_to_loc(2911, 2915, 3484, 3488, 2913, 3486)
druidic_ritual.main()
util_functions.tab_to_varrock()
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id_override': 'necklace of passage(5)', 'quantity': 5},
    {'id': osrs.item_ids.ItemIDs.LUMBRIDGE_TELEPORT.value, 'quantity': 10},
])
quest_items = [
    {
        'id': osrs.item_ids.ItemIDs.LUMBRIDGE_TELEPORT.value,
        'quantity': 'All'
    },
    osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE5.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
transport_functions.tab_to_lumby()
transport_functions.walk_to_loc(3208, 3214, 3209, 3211, 3210, 3210)
transport_functions.talk_to_lumby_duke()
rune_mysteries.main()
util_functions.tab_to_varrock()
transport_functions.walk_to_loc(3247, 3251, 3447, 3450, 3248, 3448)
util_functions.walk_through_door(24428, 'y', 4800, True, door_type='game', timeout=3)
natural_history_quiz.main()
util_functions.walk_through_door(24427, 'y', 4800, False, door_type='game', timeout=3)
transport_functions.walk_to_ge()
# buy items for waterfall, gnome stronghold, biohazard, tree gnome village, and monks friend quest
osrs.bank.ge_handler([
    # Waterfall quest
    {'id': osrs.item_ids.ItemIDs.WATER_RUNE.value, 'quantity': 10},
    {'id': osrs.item_ids.ItemIDs.AIR_RUNE.value, 'quantity': 10},
    {'id': osrs.item_ids.ItemIDs.ROPE.value, 'quantity': 10},
    {'id_override': 'Games necklace(8)', 'quantity': 3},
    {'id_override': 'Skills necklace(6)', 'quantity': 1},
    {'id_override': 'Ring of dueling(8)', 'quantity': 1},
    # grand tree
    {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 2000},
    {'id': osrs.item_ids.ItemIDs.KHAZARD_TELEPORT.value, 'quantity': 2},
    # plague city
    {'id': osrs.item_ids.ItemIDs.DWELLBERRIES.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.SPADE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.CHOCOLATE_DUST.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.SNAPE_GRASS.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.BUCKET_OF_MILK.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value, 'quantity': 4},
    # monks friend and tree gnome vilalge
    {'id': osrs.item_ids.ItemIDs.LOGS.value, 'quantity': 7},
    {'id': osrs.item_ids.ItemIDs.JUG_OF_WATER.value, 'quantity': 1},
    {'id_override': 'prayer potion(4)', 'quantity': 3},
])
quest_items = [
    osrs.item_ids.ItemIDs.GAMES_NECKLACE8.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING8.value,
    osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    osrs.item_ids.ItemIDs.ROPE.value,
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
transport_functions.walk_to_loc(3253, 3258, 3476, 3480, 3255, 3478)
util_functions.recharge_prayer_at_alter()
transport_functions.games_neck_to_barb()
transport_functions.walk_to_loc(2528, 2530, 3494, 3497, 2529, 3495)
waterfall_quest.main()
transport_functions.necklace_of_passage_tele_outpost()
transport_functions.walk_to_loc(2458, 2462, 3379, 3382, 2460, 3381)
util_functions.help_femi()
transport_functions.walk_to_loc(2473, 2476, 3436, 3440, 2474, 3438)
gnome_v2.main(25)
osrs.move.go_to_loc(2465, 3489)
grand_tree.main()
osrs.move.interact_with_object(17385, 'y', 5000, False, timeout=6, right_click_option='Climb-up')
osrs.move.interact_with_object(16683, 'z', 1, True, timeout=4)
osrs.move.go_to_loc(2449, 3483, 1)
quest_items = [
    osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
    osrs.item_ids.ItemIDs.JUG_OF_WATER.value,
    {
        'id': [
            osrs.item_ids.ItemIDs.MIND_RUNE.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.FIRE_RUNE.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION3.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION2.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION1.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION3.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION2.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION1.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.LOGS.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.RING_OF_DUELING8.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING7.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING6.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING5.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING4.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING3.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING2.value,
            osrs.item_ids.ItemIDs.RING_OF_DUELING1.value,
        ],
        'quantity': '1'
    },
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
transport_functions.dueling_to_c_wars()
transport_functions.walk_out_of_c_wars()
osrs.move.go_to_loc(2520, 3158)
osrs.move.interact_with_object(2186, 'y', 3161, True, obj_type='wall', timeout=5, right_click_option='Squeeze-through')
osrs.move.go_to_loc(2536, 3166)
tree_gnome_village.main()
osrs.move.go_to_loc(2517, 3163, right_click=True)
osrs.move.interact_with_object(2186, 'y', 3160, False, obj_type='wall', timeout=5,
                               right_click_option='Squeeze-through')
util_functions.talk_to_npc('elkoy')
util_functions.dialogue_handler([])
osrs.move.go_to_loc(2606, 3220, right_click=True)
monks_friend.main()
osrs.move.go_to_loc(2643, 3283)
osrs.clock.random_sleep(2, 2.1)
quest_items = [
    osrs.item_ids.ItemIDs.DWELLBERRIES.value,
    osrs.item_ids.ItemIDs.SPADE.value,
    osrs.item_ids.ItemIDs.ROPE.value,
    osrs.item_ids.ItemIDs.BUCKET_OF_MILK.value,
    osrs.item_ids.ItemIDs.CHOCOLATE_DUST.value,
    osrs.item_ids.ItemIDs.SNAPE_GRASS.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    {
        'id': [
            osrs.item_ids.ItemIDs.BUCKET_OF_WATER.value,
        ],
        'quantity': 'All'
    },
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
osrs.move.go_to_loc(2567, 3333)
plague_city.main()
util_functions.tab_to_varrock()
transport_functions.walk_to_ge()
util_functions.equip_item(osrs.item_ids.ItemIDs.ARDOUGNE_TELEPORT_SCROLL.value)
osrs.bank.ge_handler([
    {'id': osrs.item_ids.ItemIDs.TINDERBOX.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.LOGS.value, 'quantity': 75},
    {'id': osrs.item_ids.ItemIDs.OAK_LOGS.value, 'quantity': 200},
])
burn_logs_varrock.main(15, osrs.item_ids.ItemIDs.LOGS.value)
burn_logs_varrock.main(30, osrs.item_ids.ItemIDs.OAK_LOGS.value)
# prob need to go back to varrock and buy shit to do sea slug, knights sword,
# a quest for some thiving xp, farming xp, and dnetering the abyss mini quest
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id': osrs.item_ids.ItemIDs.SWAMP_PASTE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.UNLIT_TORCH.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.BLACK_PICKAXE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.REDBERRY_PIE.value, 'quantity': 1},
    {'id_override': 'prayer potion(4)', 'quantity': 5},
    {'id': osrs.item_ids.ItemIDs.IRON_BAR.value, 'quantity': 2},
    {'id': osrs.item_ids.ItemIDs.ARDOUGNE_TELEPORT.value, 'quantity': 5},
])
quest_items = [
    osrs.item_ids.ItemIDs.SWAMP_PASTE.value,
    osrs.item_ids.ItemIDs.UNLIT_TORCH.value,
    osrs.item_ids.ItemIDs.BLACK_PICKAXE.value,
    osrs.item_ids.ItemIDs.REDBERRY_PIE.value,
    osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    {
        'id': [
            osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value,
        ],
        'quantity': '5'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.IRON_BAR.value,
        ],
        'quantity': 'All'
    },
{
        'id': [
            osrs.item_ids.ItemIDs.ARDOUGNE_TELEPORT.value,
        ],
        'quantity': 'All'
    },
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
transport_functions.tab_to_ardy()
osrs.move.go_to_loc(2710, 3306)
sea_slug.main()
transport_functions.tab_to_fally()
osrs.move.go_to_loc(2970, 3341, right_click=True)
knights_sword.main()
transport_functions.tab_to_ardy()
osrs.move.go_to_loc(2653, 3281)
osrs.clock.random_sleep(4, 4.1)
quest_items = [
    osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
    osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
    {
        'id': [
            osrs.item_ids.ItemIDs.MIND_RUNE.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.FIRE_RUNE.value,
        ],
        'quantity': 'All'
    },
    {
        'id': [
            osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION3.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION2.value,
            osrs.item_ids.ItemIDs.PRAYER_POTION1.value,
        ],
        'quantity': 'All'
    },

    {
        'id': [
            osrs.item_ids.ItemIDs.COINS_995.value,
        ],
        'quantity': 'X',
        'amount': '1000'
    },
]
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': quest_items}]
})
util_functions.equip_staff_and_set_autocast(osrs.item_ids.ItemIDs.STAFF_OF_AIR.value, '201,1,4')
osrs.move.go_to_loc(2606, 3210)
util_functions.recharge_prayer_at_alter()
osrs.move.go_to_loc(2565, 3201)
fight_arena.main()
osrs.move.tab_to_varrock()
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id': osrs.item_ids.ItemIDs.ARROW_SHAFT.value, 'quantity': 7000},
    {'id': osrs.item_ids.ItemIDs.FEATHER.value, 'quantity': 7000},
])
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': '', 'items': [
        {
            'id': [
                osrs.item_ids.ItemIDs.FEATHER.value,
            ],
            'quantity': 'All'
        },
        {
            'id': [
                osrs.item_ids.ItemIDs.ARROW_SHAFT.value,
            ],
            'quantity': 'All'
        },
    ]}]
})
osrs.move.go_to_loc(3265, 3415)
steal_tea_and_make_arrow_shafts.main(29)
transport_functions.walk_to_ge()
osrs.bank.banking_handler({
    'dump_inv': True
})
osrs.bank.ge_handler([
    {'id_override': 'guam potion (unf)', 'quantity': 887},
    {'id': osrs.item_ids.ItemIDs.EYE_OF_NEWT.value, 'quantity': 887},
    {'id': osrs.item_ids.ItemIDs.MOLTEN_GLASS.value, 'quantity': 1000},
    {'id': osrs.item_ids.ItemIDs.IRON_DART.value, 'quantity': 2000},
    {'id': osrs.item_ids.ItemIDs.RAW_SARDINE.value, 'quantity': 600},
    {'id': osrs.item_ids.ItemIDs.STEEL_NAILS.value, 'quantity': 2000},
    {'id': osrs.item_ids.ItemIDs.HAMMER.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.SAW.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.BAGGED_DEAD_TREE.value, 'quantity': 653},
    {'id': osrs.item_ids.ItemIDs.PLANK.value, 'quantity': 588},
    {'id': osrs.item_ids.ItemIDs.PLANK.value, 'quantity': 588},
    {'id': osrs.item_ids.ItemIDs.WATERING_CAN.value, 'quantity': 3},
    {'id': osrs.item_ids.ItemIDs.PURE_ESSENCE.value, 'quantity': 1000},
    {'id': osrs.item_ids.ItemIDs.FALADOR_TELEPORT.value, 'quantity': 45},
    {'id': osrs.item_ids.ItemIDs.AIR_TIARA.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.GLASSBLOWING_PIPE.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.TROUT.value, 'quantity': 50},
])
osrs.bank.banking_handler({
    'dump_inv': True,
    'withdraw': [{'items': [
        {
            'id': osrs.item_ids.ItemIDs.GLASSBLOWING_PIPE.value,
            'quantity': '1'
        },
        {
            'id': osrs.item_ids.ItemIDs.MOLTEN_GLASS.value,
            'quantity': 'All'
        },
    ]}]
})
blow_glass_v3.main(random.randint(33, 36))
make_pots_v2.main(osrs.item_ids.ItemIDs.GUAM_POTION_UNF.value, osrs.item_ids.ItemIDs.EYE_OF_NEWT.value, random.randint(32, 34))
osrs.bank.banking_handler({
    'set_quantity': '1',
    'dump_equipment': True,
    'dump_inv': True,
    'withdraw': [{'items': [
        osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
        osrs.item_ids.ItemIDs.LUMBRIDGE_TELEPORT.value,
        osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
        {
            'id': osrs.item_ids.ItemIDs.IRON_DART.value,
            'quantity': 'All'
        },
        {
            'id': osrs.item_ids.ItemIDs.MIND_RUNE.value,
            'quantity': 'All'
        },
        {
            'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value,
            'quantity': 'All'
        },
        {
            'id': osrs.item_ids.ItemIDs.COINS_995.value,
            'quantity': 'X',
            'amount': '10000'
        },
        {
            'id': osrs.item_ids.ItemIDs.TROUT.value,
            'quantity': 'All'
        },
    ]}]
})
util_functions.equip_staff_and_set_autocast(
    osrs.item_ids.ItemIDs.STAFF_OF_AIR.value, '201,1,4', defensive=True
)
transport_functions.tab_to_lumby()
osrs.move.go_to_loc(3250, 3266)
osrs.move.interact_with_object(1560, 'x', 3253, True, obj_type='wall', intermediate_tile='3261,3266,0')
early_acc_cow_killer.main([
    {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 3},
    {'id': osrs.item_ids.ItemIDs.MIND_RUNE.value, 'quantity': 1},
], osrs.item_ids.ItemIDs.IRON_DART.value)
util_functions.tab_to_varrock()
osrs.move.go_to_loc(3243, 3473)
util_functions.talk_to_npc('estate agent', right_click=True)
util_functions.dialogue_handler(['How can I get a house?', 'Yes please!'])
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id_override': 'ring of dueling(8)', 'quantity': 5},
    {'id_override': 'teleport to house', 'quantity': 50}
])
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'withdraw': [{
        'items': [
            {'id': osrs.item_ids.ItemIDs.AIR_TIARA.value, 'quantity': '1'},
        ]
    }]
})
util_functions.equip_item(osrs.item_ids.ItemIDs.AIR_TIARA.value)
osrs.bank.banking_handler({
    'withdraw': [{
        'items': [
            {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': 'All'},
            osrs.item_ids.ItemIDs.RING_OF_DUELING8.value
        ]
    }]
})
osrs.clock.random_sleep(1, 1.1)
airs_v2.main(20)
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'withdraw': [{
        'items': [
            {'id': [
                osrs.item_ids.ItemIDs.GAMES_NECKLACE8.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE7.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE6.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE5.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE4.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE3.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE2.value,
                osrs.item_ids.ItemIDs.GAMES_NECKLACE1.value,
            ], 'quantity': '1'},
        ]
    }]
})
transport_functions.games_neck_to_burthorpe()
osrs.move.go_to_loc(2907, 3545)
osrs.move.interact_with_object(
    1540, 'y', 3543, False,
    obj_type='wall', obj_tile={'x': 2907, 'y': 3544}, intermediate_tile='2907,3542,0'
)
osrs.move.interact_with_object(7257, 'z', 1, True, obj_type='ground')
osrs.move.interact_with_object(
    7259, 'y', 4983, False, obj_type='wall', intermediate_tile='3061,4980,1'
)
osrs.move.go_to_loc(3041,4969, 1)
osrs.player.toggle_run('off')
rogues_den_cooker.main(osrs.item_ids.ItemIDs.RAW_SARDINE.value, 32)
osrs.game.talk_to_npc('emerald benedict', right_click=True)
osrs.game.dialogue_handler(['Yes actually, can you help?'], timeout=1)
osrs.bank.banking_handler({
    'dump_inv': True,
    'withdraw': [{
        'items': [
            {'id': osrs.item_ids.ItemIDs.WATERING_CAN.value, 'quantity': 'All'},
            {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': '1'},
            {'id': osrs.item_ids.ItemIDs.HAMMER.value, 'quantity': '1'},
            {'id': osrs.item_ids.ItemIDs.STEEL_NAILS.value, 'quantity': 'All'},
            {'id': osrs.item_ids.ItemIDs.COINS_995.value, 'quantity': 'All'},
            {'id': osrs.item_ids.ItemIDs.SAW.value, 'quantity': '1'},
            {'id': osrs.item_ids.ItemIDs.PLANK.value, 'quantity': 'All', 'noted': True},
            {'id': osrs.item_ids.ItemIDs.BAGGED_DEAD_TREE.value, 'quantity': 'All', 'noted': True},
        ]
    }]
})
osrs.transport.house_tele(outside=True)
osrs.move.go_to_loc(2951, 3214)
wooden_chairs_v2.main(2)
plant_dead_trees.main()
build_study.main()
osrs.transport.leave_house()
transport_functions.walk_to_ge()
osrs.bank.ge_handler([
    {'id': osrs.item_ids.ItemIDs.OAK_PLANK.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.DUST_BATTLESTAFF.value, 'quantity': 1},
    {'id': osrs.item_ids.ItemIDs.LAW_RUNE.value, 'quantity': 5000},
    {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 5000},
    {'id': osrs.item_ids.ItemIDs.SOFT_CLAY.value, 'quantity': 5000},
])
osrs.bank.banking_handler({
    'dump_inv': True,
    'dump_equipment': True,
    'withdraw': [
        {
            'items': [
                {'id': osrs.item_ids.ItemIDs.HAMMER.value, 'quantity': '1'},
                {'id': osrs.item_ids.ItemIDs.SAW.value, 'quantity': '1'},
                {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': '1'},
                {'id': osrs.item_ids.ItemIDs.LAW_RUNE.value, 'quantity': 'All'},
                {'id': osrs.item_ids.ItemIDs.OAK_PLANK.value, 'quantity': '1'},
                {'id': osrs.item_ids.ItemIDs.DUST_BATTLESTAFF.value, 'quantity': '1'},
                {'id': osrs.item_ids.ItemIDs.COINS_995.value, 'quantity': 'All'},
                {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 'All'},
                {'id': osrs.item_ids.ItemIDs.SOFT_CLAY.value, 'quantity': 'All', 'noted': True},
            ]
        }
    ]
})
util_functions.equip_item(osrs.item_ids.ItemIDs.DUST_BATTLESTAFF.value)
osrs.transport.house_tele(outside=True)
build_oak_lectern.main(1)
osrs.player.toggle_run('on')
osrs.move.go_to_loc(2954, 3214)'''
util_functions.turn_off_doors_in_house()
util_functions.drop_hammer_and_saw()

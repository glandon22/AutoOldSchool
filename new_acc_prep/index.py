import cooks_assistant
import transport_functions
import util_functions
import sheep_shearer
import imp_catcher
import osrs
import witchs_potion

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
sheep_shearer.main()
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
witchs_potion.main()
transport_functions.leave_hettys_house()
util_functions.hop_to_330()
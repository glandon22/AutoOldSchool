import osrs
import slayer.transport_functions
from osrs.item_ids import ItemIDs

items = [
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.OCCULT_NECKLACE.value,
    ItemIDs.SEERS_RING.value,
    ItemIDs.OBSIDIAN_CAPE.value,
    ItemIDs.WIZARD_BOOTS.value,
    ItemIDs.ANTIDRAGON_SHIELD.value,
    ItemIDs.TRIDENT_OF_THE_SWAMP.value,
    ItemIDs.VOID_MAGE_HELM.value,
    ItemIDs.VOID_KNIGHT_TOP.value,
    ItemIDs.VOID_KNIGHT_ROBE.value,
    ItemIDs.VOID_KNIGHT_GLOVES.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,

]

'''config = {
        'dump_inv': True,
        'dump_equipment': True,
        #'withdraw': items
        'search': [{'query': 'metal_dragons', 'items': items}]
    }

osrs.bank.banking_handler(config)'''

'''#osrs.game.tele_home_fairy_ring('alr')
#slayer.transport_functions.isle_of_souls_dungeon()
qh = osrs.queryHelper.QueryHelper()
qh.set_slayer()
qh.query_backend()
print(qh.get_slayer())'''

qh = osrs.queryHelper.QueryHelper()
qh.set_var_player(['102'])
qh.query_backend()
print(qh.get_var_player('102'))
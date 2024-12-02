import osrs


def funca():
    qh = osrs.qh_v2.qh()
    qh.set_inventory()
    qh.query_backend()
    qh.set_skills({'hunter'})
    if qh.get_inventory([osrs.item_ids.BUCKET_OF_SAND, osrs.item_ids.BUCKET_OF_SANDWORMS]):
        osrs.move.fast_click_v2(
            qh.get_inventory([osrs.item_ids.BUCKET_OF_SAND, osrs.item_ids.BUCKET_OF_SANDWORMS])
        )
    if qh.get_skills('hunter') and qh.get_skills('hunter')['level'] == 35:
        return True

#osrs.move.interact_with_object_v3(27557, custom_exit_function=funca)


from combat import slayer_killer
pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)
slayer_killer.main(
    'hill giant', pot_config.asdict(), 20
)
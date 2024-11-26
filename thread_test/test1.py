import osrs

qh = osrs.qh_v2.qh()
qh.set_widgets({'161,62'})
while True:
    qh.query_backend()
    print(qh.get_widgets('161,62'))

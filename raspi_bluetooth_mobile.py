import bluetooth

target_name = "My phone"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name(bdaddr):
        target_address = bdaddr
        break
if targte_address is not None:
    print ("found target bluetooth device with address "), target_address
else:
    print ("could not find target bluetooth device nearby")

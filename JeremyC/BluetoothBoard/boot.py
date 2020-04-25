import storage

storage.remount("/", readonly=True)

m = storage.getmount("/")
m.label = "JAC"

storage.remount("/", readonly=False)

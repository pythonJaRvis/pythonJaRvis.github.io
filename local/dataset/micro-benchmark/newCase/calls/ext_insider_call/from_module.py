def ext_change(c, fn):
    def change():
        c.fn = fn

    change()

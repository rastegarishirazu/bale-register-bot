class Student:
    bale_id = ""
    name = ""
    last_name = ""

    def __init__(self, bale_id) -> None:
        self.bale_id = bale_id

    def set_name(self, name):
        self.name = name

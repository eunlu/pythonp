class Item:
    def __init__(self,item_name):
        self.name = item_name
        self.description = None

    def set_name(self,nesne_adi):
        self.name = nesne_adi
    def get_name(self):
        return self.name

    def set_description(self,item_adi):
        self.description = item_adi
    def get_description(self):
        return self.description

    def describe(self):
        print "["+self.name+"] buradadir - "+self.description
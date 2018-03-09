class Business:
    class_counter= 1
    def __init__(self, name, category, location,description):
        self.name = name
        self.category = category
        self.location = location
        self.description = description
        self.id= Business.class_counter
        Business.class_counter += 1
    def update_business(self,newname, newcategory, newlocation, newdescription):
        self.name = newname
        self.category = newcategory
        self.location = newlocation
        self.description = newdescription


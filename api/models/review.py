class Review:
    class_counter= 1
    def __init__(self, reviewbody, businessid):
        self.reviewbody = reviewbody
        self.businessid = businessid
        self.id= Review.class_counter
        Review.class_counter += 1
        

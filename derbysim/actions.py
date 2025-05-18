
class MoveAction:
    def __init__(self, subject, carrying = False, carried = False):
        self.subject = subject
        self.carrying = carrying
        self.carried = carried

class StackAction:
    def __init__(self, subject):
        self.subject = subject

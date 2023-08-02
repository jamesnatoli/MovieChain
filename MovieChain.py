# Hold the classes that we use in for our movie chain
# James Natoli, 2023

class MovieChain:
    """This is the linked list"""
    def __init__(self):
        self.head = None

    def __repr__(self):
        """Puts the links in a python list and prints with with arrows in between"""
        link  = self.head
        links = []
        while link is not None:
            links.append( links.data)
            link = link.next
        links.append("None")
        return " -> ".join( links)

class MovieLink:
    """These are the links in the linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

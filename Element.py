class Element:

    def __init__(self, k, v, i):
        self.key = k
        self.value = v
        self.index = i

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def _wipe(self):
        self.key = None
        self.value = None
        self.index = None

    def __str__(self):
        return str(self.value)

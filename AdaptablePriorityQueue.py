from Element import *

class AdaptablePriorityQueue:

    def __init__(self):
        self.APQ = list()

    def empty(self):
        return len(self.APQ) == 0

    def add(self, key, item):
        el = Element(key, item, len(self.APQ))
        self.APQ.append(el)
        self.bubble_up(el)
        return el

    def get_key(self, el):
        if el:
            return el.key
        return None

    def bubble_up(self, el):
        el_pos = el.index
        parent_pos = (el_pos-1) // 2
        if parent_pos < 0:
            parent_pos = 0
        parent = self.APQ[parent_pos]
        if parent.key > el.key:
            parent.index = el_pos
            el.index = parent_pos
            self.APQ[el_pos] = parent
            self.APQ[parent_pos] = el
            self.bubble_up(el)

    def min_child(self, el):
        el_pos = el.index
        left_child_pos = (el_pos * 2) + 1
        right_child_pos = (el_pos * 2) + 2
        if (len(self.APQ) - 1) < left_child_pos:
            return None
        lowest_child = self.APQ[left_child_pos]
        if (len(self.APQ) - 1) >= right_child_pos:
            if self.APQ[right_child_pos] < self.APQ[left_child_pos]:
                lowest_child = self.APQ[right_child_pos]
        return lowest_child

    def bubble_down(self, el):
        el_pos = el.index
        lowest_child = self.min_child(el)
        if lowest_child is not None and lowest_child < el:
            child_pos = lowest_child.index
            lowest_child.index = el_pos
            el.index = child_pos
            self.APQ[el_pos] = lowest_child
            self.APQ[child_pos] = el
            self.bubble_down(el)

    def min(self):
        return self.APQ[0]

    def update_key(self, el, newkey):
        el.key = newkey
        el_pos = el.index
        parent_pos = (el_pos-1) // 2
        if parent_pos < 0:
            parent_pos = 0
        parent = self.APQ[(el_pos-1) // 2]
        if parent > el:
            self.bubble_up(el)
        else:
            self.bubble_down(el)

    def remove_min(self):
        if len(self.APQ) > 0:
            end = self.APQ[-1]
            the_min = self.min()
            end_pos = end.index
            end.index = 0
            self.APQ[0] = end
            self.APQ.pop()  # no need to complete swap as it is being removed anyways
            if len(self.APQ) > 0:
                self.bubble_down(self.APQ[0])
            val, key = the_min.value, the_min.key
            the_min._wipe()
            return val, key

    def __str__(self):
        return str(self.APQ)

    def print_struct(self):
        for i in self.APQ:
            print(i, i.index)

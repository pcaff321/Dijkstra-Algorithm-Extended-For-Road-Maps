from Element import *

class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element
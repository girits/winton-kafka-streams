"""
Default context passed to every processor

"""
import logging

from . import _context

log = logging.getLogger(__name__)

class ProcessorContext(_context.Context):
    """
    The same processor context is shared betwen all nodes in
    a single topology instance. It takes care of forwarding
    values to downstream processors.

    """
    def __init__(self, _recordCollector):
        super().__init__()

        self.recordCollector = _recordCollector

    def forward(self, key, value):
        """
        Forward the key/value to the next node in the topology

        """
        previousNode = self.currentNode
        try:
            for child in self.currentNode.children:
                self.currentNode = child
                child.process(key, value)
        finally:
            self.currentNode = previousNode

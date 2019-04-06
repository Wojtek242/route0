from mininet.node import Switch, Node


class Router(Switch):
    """Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.

    """

    ID = 0

    def __init__(self, name, **kwargs):

        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)

        Router.ID += 1
        self.switch_id = Router.ID

    def start(self, controllers):
        pass

    def defaultIntf(self):
        if hasattr(self, "controlIntf") and self.controlIntf:
            return self.controlIntf

        return Node.defaultIntf(self)

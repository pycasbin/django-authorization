from casbin import Enforcer


class ProxyEnforcer(Enforcer):
    def __init__(self):
        # todo read configuration, initialize Enforcer...
        model = None
        adapter = None
        super.__init__(model, adapter)
        pass


enforcer = ProxyEnforcer()

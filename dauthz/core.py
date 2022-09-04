# from casbin_adapter.adapter import Adapter as CasbinAdapter
import logging

from casbin import Enforcer
from django.conf import settings

from .utils import import_class


class ProxyEnforcer(Enforcer):
    def __init__(self, enforcer_name: str, enforcer_conf: dict):
        self.name = enforcer_name
        self.enable_log = enforcer_conf["LOG"]["ENABLED"]
        self.logger = logging.getLogger(self.name)
        if not self.enable_log:
            self.logger.disabled = True

        model_type = enforcer_conf["MODEL"]["CONFIG_TYPE"]
        if model_type == "file":
            model = enforcer_conf["MODEL"]["CONFIG_FILE_PATH"]
        else:
            model = enforcer_conf["MODEL"]["CONFIG_TEXT"]
        model = str(model)

        adapter_loc = enforcer_conf["ADAPTER"]["NAME"]
        adapter_class = import_class(adapter_loc)
        adapter = adapter_class()
        super().__init__(model, adapter)

        watcher = enforcer_conf.get("WATCHER")
        if watcher:
            self.set_watcher(watcher)
        role_manager = enforcer_conf.get("ROLE_MANAGER")
        if role_manager:
            self.set_role_manager(role_manager)
        self.logger.info("Casbin enforcer initialised")


enforcer = None
enforcers = {}
enforcer_conf_list = getattr(settings, "DAUTHZ")
for item in enforcer_conf_list.items():
    name = item[0]
    conf = item[1]
    enforcers[name] = ProxyEnforcer(enforcer_name=name, enforcer_conf=conf)

enforcer = enforcers.get("DEFAULT")

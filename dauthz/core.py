# from casbin_adapter.adapter import Adapter as CasbinAdapter
import logging
import sys

from casbin import Enforcer
from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError

from .utils import import_class

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


class ProxyEnforcer(Enforcer):
    name = None
    logger = None
    enable_log = None

    def __init__(self, enforcer_name: str, enforcer_conf: dict):
        self.name = enforcer_name
        self.logger = logging.getLogger(self.name)

        model_type = enforcer_conf.get("MODEL").get("CONFIG_TYPE")
        if model_type == "file":
            model = enforcer_conf.get("MODEL").get("CONFIG_FILE_PATH")
        else:
            model = enforcer_conf.get("MODEL").get("CONFIG_TEXT")
        model = str(model)
        self.enable_log = enforcer_conf.get("LOG").get("ENABLED")

        adapter_loc = enforcer_conf.get("ADAPTER")
        policy_storage_type = enforcer_conf.get("STORAGE").get("STORAGE_TYPE")
        # if policy_storage_type == "database":
        #     adapter_args = (enforcer_conf.get("STORAGE").get("DATABASE_CONNECTION"),)
        # else:
        #     adapter_args = (enforcer_conf.get("STORAGE").get("FILE_PATH"),)
        adapter_class = import_class(adapter_loc)
        adapter = adapter_class()
        super().__init__(model, adapter)

        watcher = enforcer_conf.get("WATCHER")
        if watcher:
            self.set_watcher(watcher)
        role_manager = enforcer_conf.get("ROLE_MANAGER")
        if role_manager:
            self.set_role_manager(role_manager)
        self.logger.debug("Casbin enforcer initialised")


class ProxyEnforcers(object):
    is_init = False
    enforcer_conf_list = {}
    enforcer_list = {}

    def __init__(self, *args, **kwargs):
        if self.is_init:
            super().__init__(*args, **kwargs)
        else:
            logging.info("Deferring casbin enforcer initialisation until django is ready")

    def load_(self):
        if not self.is_init:
            logging.info("Performing deferred casbin enforcer initialisation")
            self.is_init = True
            self.enforcer_conf_list = getattr(settings, "DAUTHZ")["ENFORCERS"]
            # construct enforcer list
            for item in self.enforcer_conf_list.items():
                enforcer_name = item[0]
                enforcer_conf = item[1]
                self.enforcer_list[enforcer_name] = ProxyEnforcer(enforcer_name=enforcer_name,
                                                                  enforcer_conf=enforcer_conf)

    def __getattribute__(self, item):
        safe_methods = ["__init__", "__class__", "load_", "is_init"]
        if not super().__getattribute__("is_init") and item not in safe_methods:
            init_enforcers()
            # self.is_init = True
            # print(super().__getattribute__("is_init"))
            if not super().__getattribute__("is_init"):
                raise Exception(
                    (
                        "Calling enforcer attributes before django registry is ready. "
                        "Prevent making any calls to the enforcer on import/startup"
                    )
                )

        return super().__getattribute__(item)


def init_enforcers():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT app, name applied FROM django_migrations
                WHERE app = 'casbin_adapter' AND name = '0001_initial';
                """
            )
            row = cursor.fetchone()
            if row:
                enforcers.load_()
    except (OperationalError, ProgrammingError):
        pass


enforcers = ProxyEnforcers()

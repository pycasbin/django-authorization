from django.core.management.base import BaseCommand

from .utils import enforcers


class Command(BaseCommand):
    help = """
        Add/Get policy, 
        usage: 
            add policy: python manage.py policy  [optional: --enforcer=<enforcer_name>] add <sub> <obj> <act>
            get policy: python manage.py policy  [optional: --enforcer=<enforcer_name>] get <sub> <obj> <act>
        """

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="ADD/GET group policy")
        parser.add_argument("sub", type=str)
        parser.add_argument("obj", type=str)
        parser.add_argument("act", type=str)
        parser.add_argument("--enforcer", type=str, help="Name of Enforcer")

    def handle(self, *args, **options):
        enforcer_name = options.get("enforcer")
        if enforcer_name is None:
            enforcer_name = "DEFAULT"
        handler_enforcer = None

        try:
            handler_enforcer = enforcers[enforcer_name]
        except KeyError:
            raise Exception("Enforcer `" + enforcer_name + "` not found")

        action = options.get("action")
        action = action.upper()
        sub = options.get("sub")
        obj = options.get("obj")
        act = options.get("act")
        if action == "ADD":
            res = handler_enforcer.add_policy(sub, obj, act)
            if res is True:
                handler_enforcer.save_policy()
                self.stdout.write("Policy added")
            else:
                self.stderr.write("Policy not added success")
        elif action == "GET":
            res = handler_enforcer.enforce(sub, obj, act)
            print("{}, {}, {} ---> {}".format(sub, obj, act, res))
        else:
            self.stderr.write("Action not found")

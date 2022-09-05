from django.core.management.base import BaseCommand

from .utils import enforcers


class Command(BaseCommand):
    help = """
        Add/Get group policy,
        usage:
            add group policy: python manage.py group [optional: --enforcer=<enforcer_name>] add <user> <role> [optional:<domain>]
            get group policy: python manage.py group [optional: --enforcer=<enforcer_name>] get <user> <role> [optional:<domain>]
        """

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="Add/Check group policy")
        parser.add_argument("--enforcer", type=str, help="Name of Enforcer")
        parser.add_argument("user", type=str)
        parser.add_argument("role", type=str)
        parser.add_argument("domain", nargs="?", type=str)

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

        if action == "ADD":
            user = options.get("user")
            role = options.get("role")
            domain = options.get("domain")
            res = None
            if domain is None:
                res = handler_enforcer.add_grouping_policy(user, role)
            else:
                res = handler_enforcer.add_grouping_policy(user, role, domain)
            if res is True:
                self.stdout.write("Group policy added")
                handler_enforcer.save_policy()
            else:
                self.stderr.write("Group policy not added success")

        elif action == "CHECK":
            user = options.get("user")
            role = options.get("role")
            domain = options.get("domain")
            if domain is None:
                res = handler_enforcer.has_grouping_policy(user, role)
                self.stdout.write("User: {} ---> Role: {} ---> Result: {}".format(user, role, res))
            else:
                res = handler_enforcer.has_grouping_policy(user, role, domain)
                self.stdout.write(
                    "User: {} ---> Role: {} ---> Domain: {} ---> Result: {}".format(user, role, domain, res)
                )
        else:
            self.stderr.write("Action not found")

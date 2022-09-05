from django.core.management.base import BaseCommand

from .utils import enforcers


class Command(BaseCommand):
    help = """
    Assign/Get role to user,
    usage: 
        add role for user: python manage.py role [optional: --enforcer=<enforcer_name>] assign <user> <role>
        get roles of user: python manage.py role [optional: --enforcer=<enforcer_name>] get <user>
    """

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="ADD/GET role policy")
        parser.add_argument("--enforcer", type=str, help="Name of Enforcer")
        parser.add_argument("user", type=str)
        parser.add_argument("role", nargs="?", type=str)

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
        user = options.get("user")
        if action == "ADD":
            role = options.get("role")
            if role is None:
                raise Exception("parameter `role` is required: ADD <user> <role>")
            res = handler_enforcer.add_role_for_user(user, role)
            if res is True:
                self.stdout.write("Role assigned")
                handler_enforcer.save_policy()
            else:
                self.stderr.write("Role not assigned success")
            self.stdout.write("Role added")
        elif action == "GET":
            res = handler_enforcer.get_roles_for_user(user)
            print("user: {} ---> roles: {}".format(user, res))
        else:
            self.stderr.write("Action not found")

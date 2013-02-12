from __future__ import absolute_import

import sys, subprocess

from optparse import OptionParser

from django.core.management.base import BaseCommand

from herokuapp.settings import HEROKU_CONFIG_BLACKLIST
from herokuapp.management.commands.base import HerokuCommandMixin


class PermissiveOptionParser(OptionParser):
    
    def error(self, *args, **kwargs):
        pass


class Command(HerokuCommandMixin, BaseCommand):
    
    help = "Runs the given management command in the Heroku app environment."
    
    option_list = BaseCommand.option_list + HerokuCommandMixin.option_list
    
    def create_parser(self, prog_name, subcommand):
        return PermissiveOptionParser(
            prog = prog_name,
            usage = self.usage(subcommand),
            version = self.get_version(),
            option_list = self.option_list,
        )    
    
    def handle(self, *args, **kwargs):
        self.app = kwargs["app"]
        # Strip the herokuapp command.
        process_args = [
            arg
            for arg
            in sys.argv
            if arg != "herokuapp"
        ]
        # Format the subprocess.
        process_args = [
            u"{name}={value}".format(
                name = name,
                value = value,
            )
            for name, value
            in self.call_heroku_shell_params_command("config").items()
            if not name in HEROKU_CONFIG_BLACKLIST
        ] + process_args
        # Run the subprocess.
        subprocess.call(u" ".join(process_args), shell=True)
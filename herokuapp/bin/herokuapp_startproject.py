import sys, os, os.path, getpass, subprocess, argparse

from django.core import management


parser = argparse.ArgumentParser(
    description = "Start a new herokuapp Django project.",
)
parser.add_argument("project_name",
    help = "The name of the project to create.",
)
parser.add_argument("dest_dir",
    default = ".",
    nargs = "?",
    help = "The destination dir for the created project.",
)
parser.add_argument("-a", "--app",
    default = None,
    dest = "app",
    required = False,
    help = "The name of the Heroku app. Defaults to the project name, with underscores replaced by hyphens.",
)
parser.add_argument("--noinput", 
    action = "store_false",
    default = True,
    dest = "interactive",
    help = "Tells Django to NOT prompt the user for input of any kind.",
)


def main():
    args = parser.parse_args()
    # Generate Heroku app name.
    app_name = args.app or args.project_name.replace("_", "-")
    # Create the project.
    try:
        os.makedirs(args.dest_dir)
    except OSError:
        pass
    management.call_command("startproject",
        args.project_name,
        args.dest_dir,
        template = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project_template")),
        extensions = ("py", "txt", "slugignore", "conf", "gitignore", "sh",),
        app_name = app_name,
        user = getpass.getuser(),
    )
    # Audit and configure the project for Heroku.
    audit_args = [os.path.join(args.dest_dir, "manage.py"), "heroku_audit", "--fix"]
    if not args.interactive:
        audit_args.append("--noinput")
    audit_returncode = subprocess.call(audit_args)
    if audit_returncode != 0:
        sys.exit(audit_returncode)
    # Give some help to the user.
    print "Heroku project created."
    print "Deploy to Heroku with `./deploy.sh`"

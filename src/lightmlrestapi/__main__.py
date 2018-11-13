# -*- coding: utf-8 -*-
"""
@file
@brief Command line.
"""
import sys


def available_commands():
    """
    Returns the list of available commands.
    """
    return ["start_mlrestapi", "encrypt_pwd"]


def main():
    """
    Defines what to run when typeing the command line::

        python -m lightmlrestapi ...
    """
    args = sys.argv
    if len(args) < 2:
        print("Usage:")
        print("")
        print("    python -m lightmlrestapi <command>")
        print("")
        print("To get help:")
        print("")
        print("    python -m lightmlrestapi <command> --help")
        print("")
        print("Available commands:")
        print("")
        for a in available_commands():
            print("    " + a)
    else:
        cmd = args[1]
        cp = sys.argv.copy()
        del cp[:2]
        if cmd == 'start_mlrestapi':
            from .cli.make_ml_app import _start_mlrestapi
            _start_mlrestapi(args=cp)
        elif cmd == 'encrypt_pwd':
            from .cli.encrypt_pwd import _encrypt_pwd
            _encrypt_pwd(args=cp)
        else:
            print("Command not found: '{0}'.".format(cmd))
            print("")
            print("Available commands:")
            print("")
            for a in available_commands():
                print("    " + a)


if __name__ == "__main__":
    main()

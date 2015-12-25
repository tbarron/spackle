"""git helpers

gitr provides a collection of subcommands that I find useful in managing git
repositories.

Commands:
    gitr bv - will bump the version of the current repo as set in <path>
        (default = version.py). Options --major, --minor, --patch, --build
        (default) determine which component of the version value is bumped

    gitr dunn - will suggest what the next step to be done probably is based on
        the state of the repo.

    gitr depth - will report how far back a commitish is (number of commits
        between the one in question and the present as well as the age of the
        target committish)

    gitr dupl - will find and report any duplicate functions in the current
        tree in .py files

    gitr flix - will find and report conflicts

    gitr hook - will list available hooks (--list), install and link a hook
        (--add), show a list of installed hooks (--show), and remove hooks
        (--rm)

    gitr nodoc - will find and report any functions in the current tree in .py
        files that have no docstring

Usage:
    gitr (-h|--help|--version)
    gitr bv [(-d|--debug)] [(-q|--quiet)] [(--major|--minor|--patch|--build)] [<path>]
    gitr depth [(-d|--debug)] <commitish>
    gitr dunn [(-d|--debug)]
    gitr dupl [(-d|--debug)]
    gitr flix [(-d|--debug)] [<target>]
    gitr hook [(-d|--debug)] (--list|--show)
    gitr hook [(-d|--debug)] (--add|--rm) <hookname>
    gitr nodoc [(-d|--debug)]

Options:
    -h --help        Provide help info (display this document)
    -d --debug       Run under the debugger
    --version        Show version
    --list           List git hooks available to install
    --show           List installed git hooks
    --add            Add a hook by name
    --rm             Remove a hook by name

Arguments
    <commitish>      which object in the commit chain to check
    <hookname>       which hook to add or remove
    <path>           path for version info
    <target>         which file to examine for conflicts
"""

# -----------------------------------------------------------------------------
def main():
    """Entrypoint
    """
    opts = docopt.docopt(sys.modules[__name__].__doc__)
    if opts['--debug']:
        pdb.set_trace()

    if opts['--version']:
        sys.exit(version.__version__)

    dispatch(opts)


# -----------------------------------------------------------------------------
def dispatch(opts):
    """
    Based on the contents of *opts*, figure out what to do, introspect the
    module, and call the appropriate function.
    """
    targl = [_ for _ in opts if _[0] not in ['-', '<'] and opts[_]]
    funcname = '_'.join(['gitr', targl[0]])
    func = getattr(sys.modules[__name__], funcname)
    func(opts)


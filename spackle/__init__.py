"""spack helpers

spackle provides a collection of subcommands that help deal with
spack-installed packages.

Commands:
    spackle link - Create a symlink by default from $HOME/bin/<pkg> to
        $SPACK_ROOT/opt/spack/.../<pkg>*/bin/<pkg>

    spackle unlink - Remove a symlink by default from $HOME/bin/<pkg> pointing
        at $SPACK_ROOT/opt/spack/.../<pkg>*/bin/<pkg>

Usage:
    spackle (-h|--help|--version)
    spackle link <package> [--from <src-dir>] [--to <payload>] [--debug]
    spackle unlink <package> [--from <src-dir>] [--debug]

Options:
    -h --help        Provide help info (display this document)
    -d --debug       Run under the debugger
    --version        Show version

Arguments
    <package>        <src-dir>/<package> -> <payload>
    <src-dir>        Where to find or put the link (default=$HOME/bin)
    <payload>        What a new link should point at (default=$SPACK
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
    funcname = '_'.join(['spkl', targl[0]])
    func = getattr(sys.modules[__name__], funcname)
    func(opts)


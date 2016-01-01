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
import docopt
import glob
import os
import pdb
import sys

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


# -----------------------------------------------------------------------------
def spkl_link(opts):
    """
    Usage: spackle link <pkg> [--from <dir>] [--to <payload>]

    will create a symlink <dir>/<pkg> pointing at <payload>.

    By default, <dir> is $HOME/bin and <paylaod> is $SPACK_OPT/<pkg>*/bin/<pkg>
    """
    pkg = opts['<package>']
    home = os.getenv('HOME')
    link = linkpath(opts['<src-dir>'], pkg)
    target = payload(opts['<payload>'], pkg)
    print('os.symlink({}, {})'.format(target, link))
    os.symlink(target, link)

# -----------------------------------------------------------------------------
def spkl_unlink(opts):
    """
    Usage: spackle unlink <pkg> [--from <dir>] [--to <payload>]

    will remove a symlink <dir>/<pkg> pointing at <payload>.

    By default, <dir> is $HOME/bin and <paylaod> is $SPACK_OPT/<pkg>*/bin/<pkg>
    """
    pkg = opts['<package>']
    home = os.getenv('HOME')
    link = linkpath(opts['<src-dir>'], pkg)
    xtarget = payload(opts['<payload>'], pkg)
    if not os.path.islink(link):
        sys.exit('{0} is not a symlink'.format(link))
    rtarget = os.readlink(link)
    if os.path.dirname(rtarget) == os.path.dirname(xtarget):
        print('os.unlink({})'.format(link))
        os.unlink(link)


# -----------------------------------------------------------------------------
def linkpath(srcdir, pkg):
    """
    Construct a path from *srcdir* (or $HOME if not given) and *pkg*
    """
    home = os.getenv('HOME')
    if srcdir:
        rval = '{}/{}'.format(srcdir, pkg)
    else:
        rval = '{}/bin/{}'.format(home, pkg)
    return rval


# -----------------------------------------------------------------------------
def spack_hunt(pkg):
    """
    Try to find $SPACK_OPT
    """
    home = os.getenv('HOME')
    candidates = [os.getenv('SPACK_OPT'),
                  '{}/spack/opt/spack/*/*'.format(home),
                  '{}/.spack/opt/spack/*/*'.format(home),
                  '{}/prj/spack/opt/spack/*/*'.format(home),
                  ]
    msg = rval = None
    for ctry in candidates:
        poss = glob.glob('{}/{}-*'.format(ctry, pkg))
        if 1 == len(poss):
            rval = '{}/bin'.format(poss[0])
            return rval
        elif len(poss) < 1:
            msg = '{} not found in any of the candidate locations'.format(pkg)
        else:
            msg = 'Found more than one {} in {}'.format(pkg, ctry)
            raise StandardError(msg)
    raise StandardError(msg or "Should never happen: X != 1, !< 1, !> 1")


# -----------------------------------------------------------------------------
def payload(path, pkg):
    """
    Construct a path from *path* (or $SPACK_OPT/<pkg>*/bin if not given) and
    *pkg*
    """
    pkg_dir = spack_hunt(pkg)
    rval = path or '{}/{}'.format(pkg_dir, pkg)
    return rval

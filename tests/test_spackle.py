import glob
import os
import pdb
import spackle

def test_link_linkpath_with_srcdir():
    """
    spackle link foo --from /tmp
    """
    assert spackle.linkpath('/tmp', 'foo') == '/tmp/foo'


def test_link_linkpath_wo_srcdir():
    """
    spackle link bar
    """
    home = os.getenv('HOME')
    assert spackle.linkpath(None, 'bar') == '{}/bin/bar'.format(home)


def test_link_payload_with_path():
    """
    spackle link git --to /usr/local/bin/tclsh
    """
    assert spackle.payload('/usr/local/bin/tclsh', 'git') == '/usr/local/bin/tclsh'


def test_link_payload_wo_path():
    """
    spackle link tmux
    """
    spack_path = os.path.join(os.getenv('HOME'),
                              'prj',
                              'spack',
                              'opt',
                              'spack',
                              'darwin-x86_64',
                              'gcc-4.2.1',
                              )
    tmux_dir = glob.glob('{}/tmux-*'.format(spack_path))
    exp = '{}/bin/tmux'.format(tmux_dir.pop())
    assert spackle.payload(None, 'tmux') == exp

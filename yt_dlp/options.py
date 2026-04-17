import optparse
import os
import sys

from .version import __version__


def parseOpts(overrideArguments=None):
    def _readOptions(filename_bytes, default=[]):
        try:
            optionf = open(filename_bytes)
        except IOError:
            return default
        try:
            contents = optionf.read()
            res = contents.split()
        finally:
            optionf.close()
        return res

    def _readUserConf(package_name, default=[]):
        # Try to read user configuration file
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
        userConfFile = os.path.join(xdg_config_home, package_name, 'config')
        if not os.path.isfile(userConfFile):
            # Fallback to legacy location
            userConfFile = os.path.join(os.path.expanduser('~'), f'.{package_name}')
        userConf = _readOptions(userConfFile, default=None)
        if userConf is not None:
            return userConf, userConfFile
        return default, None

    # Actual parsing
    parser = optparse.OptionParser(
        usage='%prog [OPTIONS] URL [URL...]',
        version=__version__,
        conflict_handler='resolve',
    )

    general = optparse.OptionGroup(parser, 'General Options')
    general.add_option(
        '-h', '--help',
        action='help',
        help='Print this help text and exit',
    )
    general.add_option(
        '--version',
        action='version',
        help='Print program version and exit',
    )
    general.add_option(
        '-U', '--update',
        action='store_true', dest='update_self',
        help='Update this program to latest version',
    )
    general.add_option(
        '-i', '--ignore-errors',
        action='store_true', dest='ignoreerrors', default=False,
        help='Continue on download errors',
    )
    general.add_option(
        '--abort-on-error',
        action='store_false', dest='ignoreerrors',
        help='Abort downloading of further videos if an error occurs',
    )
    general.add_option(
        '--dump-user-agent',
        action='store_true', dest='dump_user_agent', default=False,
        help='Display the current user-agent and exit',
    )
    general.add_option(
        '--list-extractors',
        action='store_true', dest='list_extractors', default=False,
        help='List all supported extractors and exit',
    )
    general.add_option(
        '--extractor-descriptions',
        action='store_true', dest='list_extractor_descriptions', default=False,
        help='Output descriptions of all supported extractors and exit',
    )
    parser.add_option_group(general)

    network = optparse.OptionGroup(parser, 'Network Options')
    network.add_option(
        '--proxy',
        dest='proxy', default=None, metavar='URL',
        help='Use the specified HTTP/HTTPS/SOCKS proxy',
    )
    network.add_option(
        '--socket-timeout',
        dest='socket_timeout', type=float, default=None, metavar='SECONDS',
        help='Time to wait before giving up, in seconds',
    )
    network.add_option(
        '--source-address',
        metavar='IP', dest='source_address', default=None,
        help='Client-side IP address to bind to',
    )
    network.add_option(
        '-4', '--force-ipv4',
        action='store_const', const='0.0.0.0', dest='source_address',
        help='Make all connections via IPv4',
    )
    network.add_option(
        '-6', '--force-ipv6',
        action='store_const', const='::', dest='source_address',
        help='Make all connections via IPv6',
    )
    parser.add_option_group(network)

    if overrideArguments is not None:
        opts, args = parser.parse_args(overrideArguments)
    else:
        # Read system and user config files
        systemConf = _readOptions('/etc/yt-dlp.conf')
        userConf, userConfFile = _readUserConf('yt-dlp')
        commandLineConf = sys.argv[1:]
        argv = systemConf + userConf + commandLineConf
        opts, args = parser.parse_args(argv)

    return parser, opts, args

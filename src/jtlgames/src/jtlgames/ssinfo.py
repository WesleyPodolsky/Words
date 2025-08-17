"""

"""

import argparse
import logging
import sys

from jtlgames import __version__
import pygame
from pathlib import Path
from .show import SpriteShow

__author__ = "Eric Busboom"
__copyright__ = "Eric Busboom"
__license__ = "MIT"

_logger = logging.getLogger(__name__)



def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"jtlgames {__version__}",
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print(f"The {args.n}-th Fibonacci number is {fib(args.n)}")
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="SpriteSheet display tool")
    parser.add_argument("file", help="Path to the image file", type=str)
    parser.add_argument("--no-show", help="Do not display the image", action="store_true")
    parser.add_argument("-cw", "--width", help="Cell width", type=int, default=None)
    parser.add_argument("-ch", "--height", help="Cell height", type=int, default=None)
    parser.add_argument("-x", "--offset-x", help="X offset", type=int, default=0)
    parser.add_argument("-y", "--offset-y", help="Y offset", type=int, default=0)
    return parser.parse_args(args)

def main(args):
    args = parse_args(args)
    file = Path(args.file)
    if not file.exists():
        raise FileNotFoundError(f"Error: The file {file} does not exist.")


    if args.width is None and args.height is not None:
        args.width = args.height
    elif args.height is None and args.width is not None:
        args.height = args.width
    elif args.width is None and args.height is None:
        args.width = args.height = 32

    pygame.init()
    pygame.display.set_caption("SpriteSheet Test")
    screen = pygame.display.set_mode((600, 600))

    sprite_show = SpriteShow(screen, file, (args.width, args.height), (args.offset_x, args.offset_y))
    
    #img = sprite_show.compose_horiz([0, 1, 2, 3, 4, 5, 6])
    #pygame.image.save(img, file.parent / 'composed_sprite.png')

    if not args.no_show:
        sprite_show.show()

if __name__ == "__main__":
    run()

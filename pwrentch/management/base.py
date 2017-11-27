from django.core.management.base import BaseCommand

from argparse import HelpFormatter, _textwrap


class SmartHelpFormatter(HelpFormatter):
    """Better formatting for management command help text

    Allows the help text to contain new line characters if the text
    starts with 'R|' or 'r|'.

    Extends:
        HelpFormatter

    Credit:
        https://stackoverflow.com/a/43139055/645638
        https://stackoverflow.com/a/35470682/645638
    """

    def _fill_text(self, text, width, indent):
        """Formats `text` to the specified `width` and intends by `indent`

        Used to display the command's description and supports new line
        characters if `text` starts with 'r|'.

        Arguments:
            text   {string} -- String of text to be formatted
            width  {integer} -- Max width of each line of `text`
            indent {integer} -- Number of spaces to indent each line of `text`
        """
        if text.startswith('R|') or text.startswith('r|'):
            paragraphs = text[2:].splitlines()
            wrapped_paragraphs = [
                _textwrap.wrap(paragraph, width)
                for paragraph in paragraphs
            ]
            smart_help = []
            for wrapped_paragraph in wrapped_paragraphs:
                if len(wrapped_paragraph):
                    for line in wrapped_paragraph:
                        smart_help.append(line)
                else:
                    smart_help.append('')
            return '\n'.join(smart_help)
        return super(SmartHelpFormatter, self)._fill_text(text, width, indent)


    def _split_lines(self, text, width):
        """Allows `text` to contain new line characters

        Used to display the description of command line arguments and supports
        new line characters if `text` starts with 'r|'.

        Arguments:
            text  {string} -- String of text to be formatted
            width {integer} -- Max width of each line of `text`
        """
        if text.startswith('R|') or text.startswith('r|'):
            return text[2:].splitlines()
        return super(SmartHelpFormatter, self)._split_lines(text, width)




class PwrentchCommand(BaseCommand):
    """Additional features and functionality to Django's management command

    Features:
        - dryrun command line argument
        - makes dry run and verbosity available as attributes
        - provides self._write() as a standard way to output to StrOut
        - provides self._error() as a standard way to output to StrErr
        - self._write() and self._error() allow the automatic carriage return
          to be changed or supressed
        - self._write() compares against self.verbosity to determine when
          the message should be output

    Extends:
        BaseCommand
    """
    def create_parser(self, prog_name, subcommand):
        """Add dryrun command line option"""
        parser = super(PwrentchCommand, self).create_parser(prog_name, subcommand)  # NOQA
        # use the updated formatter to allow for carriage returns
        parser.formatter_class = SmartHelpFormatter
        # add the dry run command line option
        parser.add_argument(
            '-d', '--dryrun',
            action='store_true',
            default=False,
            dest='dryrun',
            help='Prevents the command from making any permanent changes',
        )
        return parser


    def _error(self, msg, end=None, verbosity=1):
        """Output a message to the standard error stream

        Arguments:
            msg {string} -- The message to output to the standard error stream

        Keyword Arguments:
            end {string} -- Override the standard string ending character
                            ('\n') to use something else. Use a blank string
                            ('') to keep the next call to `self._error` on
                            the same line in the terminal. (default: {None})
            verbosity {int} -- What verbosity level the command must be running
                               at for the message to be output (default: {1})
        """
        if self.verbosity >= verbosity:
            self.stderr.write(msg, ending=end)
            self.stderr.flush()


    def execute(self, *args, **options):
        """Convert dryrun and verbosity options to attributes

        Arguments:
            **options {dict} -- Options dict built from the command line args
        """
        self.dryrun = options['dryrun']
        self.verbosity = options['verbosity']
        super(PwrentchCommand, self).execute(*args, **options)


    def _write(self, msg, end=None, verbosity=1):
        """Output a message to the standard output stream

        Arguments:
            msg {string} -- The message to output to the standard output stream

        Keyword Arguments:
            end {string} -- Override the standard string ending character
                            ('\n') to use something else. Use a blank string
                            ('') to keep the next call to `self._write` on
                            the same line in the terminal. (default: {None})
            verbosity {int} -- What verbosity level the command must be running
                               at for the message to be output (default: {1})
        """
        if self.verbosity >= verbosity:
            self.stdout.write(msg, ending=end)
            self.stdout.flush()

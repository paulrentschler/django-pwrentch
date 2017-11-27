# Management commands

An improved version of Django's `BaseCommand` is provided to

* add the "dryrun" command line option
* make the "dryrun" and "verbosity" options into attributes
* provide an `_error()` method for outputting error messages to stderr
* provide a `_write()` method for outputting message to stdout
* ensure that both `_error()` and `_write()` respect the verbosity option
* allow the command help text (`self.help` attribute) to contain new line characters


## Import statement

    from pwrentch.management.base import PwrentchCommand


## Utilizing the dryrun option

The dryrun option is to allow the management command to be run without
it making any permanent changes to files, databases, etc. When writing the
management command, additional code will need to be added just prior to
statements making permanent changes to check for the dryrun option
(using `self.dryrun` which is a boolean). When `self.dryrun = True` it is
suggested that a message is output, prepended with "DryRun: ", to indicate
what **would** have happened.


## Providing better help text

A management command should have a `help` attribute that describes what the
command does, but the built-in support does not allow this text to include
new line characters which would improve the readability of the help message.

PwrentchCommand provides this functionality if the help text string starts
with `R|` or `r|`.

This can also be used when specifying the help text for a command line
argument using the `help` parameter of the `parser.add_argument()` function.
Prefix the help text with `R|` or `r|` to be able to use new line characters.


### Examples

    class MyCommand(PwrentchCommand):
        help = (
            "This is my management command that provides a dryrun mode and "
            "honors the verbosity setting when outputting messages."
        )

This will output the help text as:

    This is my management command that provides a dryrun mode and honors the
    verbosity setting when outputting messages.

Where as, definiting it with the `r|` option like so:

    class MyBetterCommand(PwrentchCommand):
        help = (
            "r|This is my better management command that:\n"
            "  - provides a dry run mode\n"
            "  - honors the verbosity setting when outputting messages\n"
            "  - provides a very readable help message\n"
        )

Will cause the help text look like this:

    This is my better management command that:
      - provides a dry run mode
      - honors the verbosity setting when outputting messages
      - provides a very readable help message


## Outputting text and errors

* Output errors with `self._error(msg)`
* Output normal messages with `self._write(msg)`


### Controlling when the message is output

The built-in verbosity option allows the command to specify how much output
should be displayed when the command is run. Setting `-v 0` should result
in **nothing** being output from the command run. `-v 1` is the default when
no verbosity level is specified. Additional levels include 2 and 3.

The command line specified verbosity level is contained in
`options['verbosity']` and also in `self.verbosity`.

When calling `self._error()` or `self._write()` the verbosity parameter
(`verbosity=2`) is used to indicate the minimum verbosity level needed in
order for the message to be output. This allows very detailed debugging
messages using `self._write(msg, verbosity=3)` which will only be output
when the command is run with `-v 3`.


### Displaying multiple outputs on the same line

Normally each call to `self._error()` or `self._write()` will print the message
provided and move to the next line (a carriage return). If the line being
output is going to be completed with a later statement, the carriage return
can be supressed by specifying `end=''` in the call to either output method.

#### Example

    self._write('Checking for dryrun mode: ', end='')
    if self.dryrun:
        self._write('Enabled')
    else:
        self._write('Disabled')

    # prints: Checking for dryrun mode: Enabled
    # or: Checking for dryrun mode: Disabled

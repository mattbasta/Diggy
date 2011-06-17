=======
 Diggy
=======
Version 0.5

Diggy is a tool for automated traceback testing for the amo-validator, though
it could conceivably be used to test nearly any python project that is designed
to work with files that are a part of a large directory.

The app works by traversing a directory (online or offline) and feeding the
files from those directories into the API for the amo-validator. If a traceback
occurs, a copy of the traceback is stored along with a copy of the file that
generated the traceback. Other settings allow Diggy to traverse the directory
of files that produced tracebacks and move "fixed" files (and their traceback
log file) to another directory. This can also be run on *that* directory,
enabling regression testing.

-------------
 Using Diggy
-------------

-s                  Alias to ``--source``
--source            The source of the files. May be "directory" or "fmo"
                    (default). If using "directory", the ``--directory`` option
                    must be set.
--directory         The directory to pull files from for testing. Required if
                    the source is set to "directory".
--movetofixed       If this is true, when a file does not throw a traceback, it
                    (along with its log file, if it exists) will be moved to
                    the --fixeddirectory.
--fixeddirectory    The directory to move files that do not throw tracebacks
                    (along with their logs, if present). Defaults to
                    ``fixed_tracebacks/``.
--brokendirectory   The directory to move files that throw tacebacks (along
                    with the new traceback log). Defaults to
                    ``tracebacks/``.
--cachefile         The location to store a cache of paths taken when
                    ``--source`` is set to ``fmo``. Defaults to
                    ``testcache.cache``.
--sparse            When pulling from ``fmo`` as a source, this option will
                    use the last version listed in an add-on's directory. All
                    other versions will not be tested. This is appropraite for
                    a fast test and getting an overview of the expected diggy
                    results.


Example Usage
=============

::

    # Run diggy on files.mozilla.org
    ./dig

    # Run on existing traceback to test for fixed problems
    ./dig -s directory --directory tracebacks/ --movetofixed

    # Run on fixed problems to test for regression
    ./dig -s directory --directory fixed_tracebacks

------------------
 Diggy diggy hole
------------------

::

                                                  ___I___
                                                 /=  |  #\
                                                /.__-| __ \
                                                |/ _\_/_ \|
                                                (( __ \__))
                                             __ ((()))))()) __
                                           ,'  |()))))(((()|# `.
                                          /    |^))()))))(^|   =\
                                         /    /^v^(())()()v^\'  .\
                                         |__.'^v^v^))))))^v^v`.__|
                                        /_ ' \______(()_____(   |
                                   _..-'   _//_____[xxx]_____\.-|
                                  /,_#\.=-' /v^v^v^v^v^v^v^v^| _|
                                  \)|)      v^v^v^v^v^v^v^v^v| _|
                                   ||       :v^v^v^v^v^v`.-' |#  \,
                                   ||       v^v^v^v`_/\__,--.|\_=_/
                                   ><       :v^v____|  \_____|_
                                   ||       v^      /  \       /
                               ----------   `/_..-._\   )_...__\
                               |        |     |_='_(     |  =_(_
                               |   ||   |    /     =\    /  '  =\
                                \/ \/ )/ gnv |=____#|    '=....#|

                                I AM A DWARF AND I'M DIGGING A HOLE!
                                          DIGGY DIGGY HOLE!
                                                        - Simon Lane

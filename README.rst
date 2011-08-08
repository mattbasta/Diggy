==========
 Grizwald
==========
Version 1

Grizwald is a statistics gathering tool based on CouchDB that enables better
code analysis on amo-valiator. It makes graphs and can even be set up to run
in conjunction with a CI tool, if you really wanted to.


-------------
 Using Diggy
-------------

-c                  Alias to ``--commit``
--commit            The commit being analyzed.
-s                  Alias to ``--source``
--source            The source of the files. May be "directory" (default) or
                    "fmo". If using "directory", the ``--directory`` option
                    must be set.
--directory         The directory to pull files from for testing. Required if
                    the source is set to "directory".
--cachefile         The location to store a cache of paths taken when
                    ``--source`` is set to ``fmo``. Defaults to
                    ``testcache.cache``.
--thorough          When pulling from ``fmo`` as a source, this option will
                    use ALL versions listed in an add-on's directory, rather
                    than just the latest version.
--js                Scrape JS from the add-ons.


Example Usage
=============

::

    # Run grizwald on ./cache/
    ./start -c 12345

--------------------
 Who is this again?
--------------------

    IT APPEARS I HAVE DIED! I'M WRITING THIS README FROM BEYOND THE GRAVE!
                                                        - Simon Lane


from StringIO import StringIO
import argparse
import hashlib
import mechanize
import os
import shutil
import sys
import traceback
import urllib2
import validator.validate
from validator.validate import validate


acount = 0
vcount = 0

testcache = set()

def main():
    """Figure out what's up."""

    parser = argparse.ArgumentParser(
            description="Begin digging for problems with the validator")
    parser.add_argument("-s",
                        "--source",
                        default="fmo",
                        choices=["fmo", "directory"])
    parser.add_argument("--directory",
                        help="The directory to find add-ons in.",
                        required=False)
    parser.add_argument("--movetofixed",
                        const=True,
                        action="store_const",
                        help="If the validation passes, move the add-on to "
                             "the fixed tracebacks folder")
    args = parser.parse_args()

    if args.source == "fmo":
        start_fmo()
    else:
        if not args.directory:
            print "No directory provided."
            return

        for fname in os.listdir(args.directory):
            if fname == ".DS_Store":
                continue
            elif not fname.endswith((".jar", ".xpi")):
                continue

            print fname
            path = os.path.join(args.directory, fname)
            val_result = _validate(path, fname)
            if val_result and args.movetofixed:
                shutil.move(path, "fixed_tracebacks/%s" % fname)
                shutil.move("%s.log" % path, "fixed_tracebacks/%s.log" % fname)


def start_fmo():
    """Begin iterating ftp.mozilla.com and find add-ons to validate."""

    global acount, testcache

    print "I AM A DWARF AND I'M RUNNING SOME TESTS! RUNNY RUNNY TESTS!"

    # Load up previous caches of properly validated add-ons.
    print "Loading test cache..."
    try:
        testcachedata = open("testcache.cache").read()
        for line in testcachedata.split("\n"):
            testcache.add(line.strip())
    except:
        raise
        testcache = set()

    br = mechanize.Browser()
    br.open("http://ftp.mozilla.org/pub/mozilla.org/addons/")
    for addon_link in list(br.links()):
        if addon_link.url.startswith("/") or addon_link.url.count("?"):
            continue
        print addon_link
        acount += 1
        br.follow_link(addon_link)
        handle_addon_directory(br)


def handle_addon_directory(br):
    """Iterates through each version of an add-on and validates it."""

    global vcount
    for version_link in br.links():
        if version_link.url.count("?") or version_link.url.startswith("/"):
            continue
        vcount += 1

        download_and_validate("%s%s" % (version_link.base_url,
                                        version_link.url),
                              version_link.url)


def download_and_validate(link, name):
    """Downloads an add-on and performs the validation."""

    link_hash = hashlib.md5(link).hexdigest()
    if link_hash in testcache:
        print "Cached (skipping): %s" % link
        return

    print "Downloading %s" % link

    # Download
    request = urllib2.urlopen(link)
    extension = link.split(".")[-1]
    path = "/tmp/validate.%s" % extension
    output = open(path, "w")
    output.write(request.read())
    output.close()

    _validate(path, name)

    testcache.add(link_hash)
    open("testcache.cache", mode="a").write("\n%s" % link_hash)


def _validate(path, name):
    """Perform steps necessary to complete a basic validation."""

    print "Validating..."

    s = sys.stdout
    sys.stdout = StringIO()
    toprint = []

    result = True

    try:
        validator.validate.validator.loader.validator.testcases.content.testendpoint_js.traverser.DEBUG = True
        json = validate(path=path)
        output = sys.stdout.getvalue()

        toprint.append("JSON Length: %d; stdout Length: %d" % (len(json),
                                                               len(output)))

        toprint.append("Done - %d/%d" % (acount, vcount) if json else json)
    except Exception as ex:
        tback = open("tracebacks/%s.log" % name, mode="w")
        traceback.print_exc(file=tback)
        tback.close()

        traceback_path = "tracebacks/%s" % name
        if path != traceback_path:
            shutil.move(path, traceback_path)
        toprint.append("FAILURE WITH TRACEBACK: %s" % ("%s.log" %
                                                traceback_path))
        result = False

    sys.stdout = s
    print "\n".join(toprint)

    return result


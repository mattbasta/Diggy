from StringIO import StringIO
import argparse
import hashlib
import mechanize
import os
import shutil
import sys
import time
import traceback
import urllib2
import validator.validate

import couchdb
import mechanize
from validator.validate import validate


testcache = set()

def main():
    """Figure out what's up."""
    global testcache

    parser = argparse.ArgumentParser(
            description="Begin digging for problems with the validator")
    parser.add_argument("-s",
                        "--source",
                        default="fmo",
                        choices=["fmo", "directory"])
    parser.add_argument("--directory",
                        help="The directory to find add-ons in.",
                        required=False,
                        default="cache/")
    parser.add_argument("--cachefile",
                        help="The path to the test cache.",
                        required=False,
                        default="testcache.cache")
    parser.add_argument("--thorough",
                        const=True,
                        help="Running in thorough mode will download all "
                             "versions of an add-on when running from "
                             "--source fmo.",
                        action="store_const")
    parser.add_argument("--js",
                        const=True,
                        help="Running this will scrape JS information from "
                             "the add-ons.",
                        action="store_const")
    args = parser.parse_args()

    print "I'm PROFESSOR GRIZZZWALLLDDDDDD!"

    if args.source == "fmo":
        # Load up previous caches of properly validated add-ons.
        try:
            testcachedata = open(args.cachefile).read()
            for line in testcachedata.split("\n"):
                testcache.add(line.strip())
        except IOError:
            testcache = set()

        br = mechanize.Browser()
        br.open("http://ftp.mozilla.org/pub/mozilla.org/addons/")
        for addon_link in list(br.links()):
            if addon_link.url.startswith("/") or addon_link.url.count("?"):
                continue
            print addon_link.url

            # Test if it's in the cache already.
            link_hash = hashlib.md5(addon_link.url).hexdigest()
            if link_hash in testcache:
                print "Cached (skipping)"
                continue

            br.follow_link(addon_link)
            handle_addon_directory(br, args)

            # Add the URL to the cache.
            testcache.add(link_hash)
            open(args.cachefile, mode="a").write("\n%s" % link_hash)

    else:
        if not args.directory:
            print "No directory provided."
            return

        for fname in os.listdir(args.directory):
            if fname == ".DS_Store":
                continue
            elif not fname.endswith((".jar", ".xpi")):
                continue

            path = os.path.join(args.directory, fname)
            val_result = _validate(path, fname, args)
            if val_result and args.movetofixed:
                shutil.move(path, "%s%s" % (args.fixeddirectory, fname))
                shutil.move("%s.log" % path, "%s%s.log" %
                                                 (args.fixeddirectory, fname))


def handle_addon_directory(br, args):
    """Iterates through each version of an add-on and validates it."""

    links = []
    for version_link in br.links():
        if version_link.url.count("?") or version_link.url.startswith("/"):
            continue

        url = "%s%s" % (version_link.base_url, version_link.url)

        if not args.thorough:
            links.append((url, version_link.url))
        else:
            download_and_validate(url, version_link.url, args)

    if not args.thorough and links:
        url, name = links.pop()
        download_and_validate(url, name, args)


def download_and_validate(link, name, args):
    """Downloads an add-on and performs the validation."""

    # Add some safety to the name.
    if not name[0].isalnum():
        name = "_%s" % name

    request = urllib2.urlopen(link)
    extension = link.split(".")[-1]

    # Put the extension where it belongs.
    path = "%s%s" % (args.directory, name)
    output = open(path, "w")
    output.write(request.read())
    output.close()

    _validate(path, name, args)


def _validate(path, name, args):
    """Perform steps necessary to complete a basic validation."""

    s = sys.stdout
    sys.stdout = StringIO()
    toprint = ["Validating %s" % name]

    couch = couchdb.Server()
    start_time = time.time()

    output = {}

    try:
        err = validate(path=path, scrape=args.js, format=None)
        output = json.loads(err.render_json())

    except:
        output = {"error": True,
                  "traceback": traceback.format_exc()}

    else:
        # Save scraped JS.
        if args.js:
            js_db = couch["grizwald_js"]

            js_files = err.get_resource("js")
            if js_files:
                for js_file in js_files:
                    js_db.save({"blob": js_file,
                                "type": "js",
                                "path": path,
                                "now": start_time})

            js_identifiers = err.get_resource("js_identifiers")
            if js_identifiers:
                js_db.save({"blob": list(js_identifiers),
                            "type": "identifiers",
                            "path": path,
                            "now": start_time})

        output["hard_output"] = sys.stdout.get_value()

    finally:
        end_time = time.time()

        output["now"] = end_time
        output["path"] = path
        output["duration"] = end_time - start_time

        couch["grizwald"].save(output)

    sys.stdout = s
    print "\n".join(toprint)


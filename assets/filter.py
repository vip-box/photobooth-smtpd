#!/usr/bin/env python3

import sys
import subprocess
from email.parser import Parser

# from email.utils import parseaddr, formataddr
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="/tmp/content-filter.log",
    filemode="a",
)

DEBUG = False
LOOP_HEADER = "X-Filter-Loop"
EX_TEMPFAIL = 75
EX_UNAVAILABLE = 69


def apply_filter(frm, rewrite_to, to, content):
    content["X-To"] = ",".join(to)
    return frm, rewrite_to, to, content


def parse_args():
    try:
        cli_from = sys.argv[1].lower()
        cli_rewrite_to = sys.argv[2].lower()
        cli_to = [x.lower() for x in sys.argv[3:]]
    except IndexError:
        sys.exit(EX_UNAVAILABLE)
    else:
        if DEBUG:
            logging.debug(
                "From: %s / Rewrite_to: %s / To: %r"
                % (cli_from, cli_rewrite_to, cli_to)
            )
        return cli_from, cli_rewrite_to, cli_to


def re_inject(frm, rewrite_to, to, content):
    if LOOP_HEADER in content:
        return True
    content[LOOP_HEADER] = "yes"

    TO = [x.lower() for x in rewrite_to.split(",")]
    if rewrite_to == "None":
        TO = to

    if DEBUG:
        logging.debug("Delivery From: %s / To: %r" % (frm, TO))

    p = subprocess.Popen(
        ["/usr/sbin/sendmail", "-G", "-i", "-f", frm] + TO,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    (stdout, stderr) = p.communicate(content.as_bytes())
    ret = p.wait()

    if ret == 0:
        if DEBUG:
            logging.debug(
                "Mail resent via sendmail, stdout: %s, stderr: %s" % (stdout, stderr)
            )
        return True
    try:
        logging.error(
            "Error re-injectin via sendmail, stdout: %s, stderr: %s" % (stdout, stderr)
        )
        logging.error("From: %s / To: %r" % (frm, to))
    except Exception:
        logging.error("Logging Error...")
    return False


def main():
    frm, rewrite_to, to = parse_args()
    content = Parser().parsestr("".join(sys.stdin.readlines()))

    # if DEBUG:
    #     logging.debug("email source : %s" % content.as_string())

    if not re_inject(*apply_filter(frm, rewrite_to, to, content)):
        sys.exit(EX_TEMPFAIL)


if __name__ == "__main__":
    main()

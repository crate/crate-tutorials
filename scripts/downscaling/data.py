#!/usr/bin/env python3

import random
import string
import ipaddress
import time


# to achieve log lines as in:
#     2012-01-01T00:00:00Z,25.152.171.147,/crate/Five_Easy_Pieces.html,200,280278
# -> timestamp,
# -> random ip address,
# -> random request (a path),
# -> random status code,
# -> random object size,


def timestamp_range(start, end, format):
    st = int(time.mktime(time.strptime(start, format)))
    et = int(time.mktime(time.strptime(end, format)))
    dt = 1 # 1 sec
    fmt = lambda x: time.strftime(format, time.localtime(x))
    return (fmt(x) for x in range(st, et, dt))


def rand_ip():
    return str(ipaddress.IPv4Address(random.getrandbits(32)))


def rand_request():
    rand = lambda src: src[random.randint(0, len(src) - 1)]
    path = lambda: "/".join((rand(("usr", "bin", "workspace", "temp", "home", "crate"))) for _ in range(4))
    name = lambda: ''.join(random.sample(string.ascii_lowercase, 7))
    ext = lambda: rand(("html", "pdf", "log", "gif", "jpeg", "js"))
    return "{}/{}.{}".format(path(), name(), ext())


def rand_object_size():
    return str(random.randint(0, 1024))


def rand_status_code():
    return str(random.randint(100, 500))


if __name__ == "__main__":
    print("log_time,client_ip,request,status_code,object_size")
    for ts in timestamp_range("2019-01-01T00:00:00Z", "2019-01-01T01:00:00Z", '%Y-%m-%dT%H:%M:%SZ'):
        print(",".join([ts, rand_ip(), rand_request(), rand_status_code(), rand_object_size()]))

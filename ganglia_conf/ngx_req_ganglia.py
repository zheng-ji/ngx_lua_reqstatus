#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import requests

def metric_handler(name):
    r = requests.get("http://localhost:6062/info")
    respstr = r.text
    arr = respstr.split('\n')
    metric_handler.info = {}

    for item in arr[:-1]:
        tmp = item.split(':')
        n, value= tmp[0],tmp[1]
        if n == 'Goroutine Num':
            metric_handler.info['goroutine_num'] = int(value.strip())
        if n == 'QPS':
            metric_handler.info['qps'] = int(value.strip())
        if n == 'MemStats NumGC':
            metric_handler.info['NumGC'] = int(value.strip())
        if n == 'PersisWrite(ms)':
            metric_handler.info['PersisWrite'] = float(value.strip())
        if n == 'PersisRead(ms)':
            metric_handler.info['PersisRead'] = float(value.strip())
        if n == 'InternalCacheRead (ms)':
            metric_handler.info['InternalCacheRead'] = float(value.strip())
        if n == 'clustercacheRead (ms)':
            metric_handler.info['clustercacheRead'] = float(value.strip())
        if n == 'hkeys (ms)':
            metric_handler.info['hkeys'] = float(value.strip())
        if n == 'hgetall (ms)':
            metric_handler.info['hgetall'] = float(value.strip())
        if n == 'hmset (ms)':
            metric_handler.info['hmset'] = float(value.strip())
        if n == 'del (ms)':
            metric_handler.info['del'] = float(value.strip())
        if n == 'Cache HitRate':
            metric_handler.info['hitrate'] = float(value.strip()) * 100
    return metric_handler.info.get(name, 0)


def metric_init(params={}):
    metrics = {
        "hitrate" : {"units": "%"},
        "qps" : {"units": ""},
        "goroutine_num": {"units": ""},
        "NumGC" : {"units": ""},
        "PersisWrite": {"units": "ms"},
        "PersisRead" : {"units": "ms"},
        "InternalCacheRead": {"units": "ms"},
        "clustercacheRead" : {"units": "ms"},
        "hkeys": {"units": "ms"},
        "hgetall" : {"units": "ms"},
        "hmset": {"units": "ms"},
        "del": {"units": "ms"},
    }

    metric_handler.descriptors = {}
    for name, updates in metrics.iteritems():
        descriptor = {
            "name"      : name,
            "call_back" : metric_handler,
            "time_max"  : 90,
            "value_type": "float",
            "units"     : "",
            "slope"     : "both",
            "format"    : "%.3f",
            "description": "http://www.youmi.net",
            "groups"    : "cpasvr",
        }
        descriptor.update(updates)
        metric_handler.descriptors[name] = descriptor
    return metric_handler.descriptors.values()

def metric_cleanup():
    pass

if __name__ == "__main__":
    desc = metric_init({})
    print "name\tvalue"
    for d in desc:
        v = d['call_back'](d['name'])
        print '%s\t %s' % (d['name'], v)

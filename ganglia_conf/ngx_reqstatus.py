#!/usr/bin/env python
# -*- coding: utf-8 -*-
# zheng-ji.info

import os
import requests

def metric_handler(name):
    r = requests.get("http://localhost:6080/?domain=xxxxx")
    respstr = r.text
    arr = respstr.split('\n')
    metric_handler.info = {}

    for item in arr[:-1]:
        tmp = item.split(':')
        n, value= tmp[0],tmp[1]
        if n == 'Request Count:
            metric_handler.info['request_count'] = int(value.strip())
        if n == 'Requests Per Secs':
            metric_handler.info['qps'] = int(value.strip())
        if n == '5xx num':
            metric_handler.info['5xx_num'] = int(value.strip())
        if n == 'Average Req Time':
            metric_handler.info['avg_req_time'] = float(value.strip())
    return metric_handler.info.get(name, 0)


def metric_init(params={}):
    metrics = {
        "request_count" : {"units": ""},
        "qps" : {"units": ""},
        "5xx_num": {"units": ""},
        "avg_req_time" : {"units": "s"},
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
            "groups"    : "ngx_reqstatus",
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

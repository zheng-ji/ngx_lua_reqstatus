#!/usr/bin/env python
# -*- coding: utf-8 -*-
# zheng-ji

import requests


def metric_handler(name):
    arr = metric_handler.result_from_http
    metric_handler.info = {}

    for item in arr[:-1]:
        tmp = item.split(':')
        n, value = tmp[0], tmp[1]
        if n == 'Request Count':
            metric_handler.info['request_count'] = int(value.strip())
        if n == 'Requests Per Secs':
            metric_handler.info['qps'] = float(value.strip())
        if n == '5xx num':
            metric_handler.info['5xx_num'] = int(value.strip())
        if n == 'Average Req Time Sec':
            metric_handler.info['avg_req_time'] = float(value.strip()) * 1000
    return metric_handler.info.get(name, 0)


def metric_init(params={}):
    metric_handler.host = params.get("host", "127.0.0.1")
    metric_handler.port = params.get("port", "6080")
    url = "http://localhost:%s/?domain=%s" % (
        metric_handler.port, metric_handler.host)
    r = requests.get(url)
    respstr = r.text
    metric_handler.result_from_http = respstr.split('\n')

    metrics = {
        "request_count": {"units": ""},
        "qps": {"units": ""},
        "5xx_num": {"units": ""},
        "avg_req_time": {"units": "ms"},
    }

    metric_handler.descriptors = {}
    for name, updates in metrics.iteritems():
        descriptor = {
            "name": name,
            "call_back": metric_handler,
            "time_max": 90,
            "value_type": "float",
            "units": "",
            "slope": "both",
            "format": "%.3f",
            "description": "http://www.youmi.net",
            "groups": "ngx_reqstatus",
        }
        descriptor.update(updates)
        metric_handler.descriptors[name] = descriptor
    return metric_handler.descriptors.values()


def metric_cleanup():
    pass

if __name__ == "__main__":
    desc = metric_init({"host": "justforfun.com", "port": "6080"})
    print "name\tvalue"
    for d in desc:
        v = d['call_back'](d['name'])
        print '%s\t %s' % (d['name'], v)

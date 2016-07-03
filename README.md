
## ngx_lua_reqstatus

实时监控 Nginx 域名的 qps, 5xx 个数，响应时长, 其中 `ganglia_conf` 目录是 ganglia 监控脚本。

#### 配置 `nginx.conf`

```shell
http {
    ...
    ...

    lua_shared_dict statics_dict    1M; # 初始化变量
    lua_package_path "/etc/nginx/ngx_lua_reqstatus/?.lua";  #路径
    log_by_lua_file "/etc/nginx/ngx_lua_reqstatus/hook.lua"; #  添加此句

    server {
        listen 80;
        server_name  justforfun.com; 
        location /{
            ...
        }
    }

    # 监控服务
    server {
        listen 127.0.0.1:6080;
        location /{
            content_by_lua_file "/etc/nginx/ngx_lua_reqstatus/status.lua";
        }
    }
}
```

#### 效果

* 查看 域名 `justforfun.com` 的qps,5xx个数，平均响应时长:

![ganglia](https://cloud.githubusercontent.com/assets/1414745/15242755/72910f62-192a-11e6-9a6c-8cc2d2c05216.png)

```
curl localhost:6080/?domain=justforfun.com
```

* 输出

```
Server Name key:    justforfun.com
Seconds SinceLast:  26.601999998093
Average Req Time Sec:   0.031799983978271
Request Count:  5
Requests Per Secs:  0.18795579281101
5xx num:    0
```

* 如果对你有帮助, 请我喝杯咖啡吧 :)

![wechatqr](https://cloud.githubusercontent.com/assets/1414745/15242713/42270b10-192a-11e6-9d37-0e538089e3d0.png)

license
-------

MIT License.

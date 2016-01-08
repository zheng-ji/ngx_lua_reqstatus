
## ngx_lua_reqstatus

实时监控 Nginx 域名的 qps, 5xx 个数，响应时长, 其中 `ganglia_conf` 目录是 ganglia 监控脚本。

#### 配置 `nginx.conf`

```shell
http {
    ...
    ...

    lua_shared_dict statics_dict    1M; # 初始化变量
    lua_package_path "/etc/nginx/ngx_lua_reqstatus/?.lua";  #路径

    server {
        listen 80;
        server_name  justforfun.com; 

        # 在需要监控的 server_name 添加此句
        log_by_lua_file "/etc/nginx/ngx_lua_reqstatus/hook.lua";
        location /{
            ...
            ...
        }
    }
    # 监控服务
    server {
        listen 127.0.0.1:6080;
        location /{
            access_by_lua_file "/etc/nginx/ngx_lua_reqstatus/status.lua";
        }
    }
}
```

#### 效果

* 查看 域名 `justforfun.com` 的qps,5xx个数，平均响应时长:

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


license
-------

MIT License.

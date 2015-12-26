
## ngx_reqstatus_lua

实时监控 Nginx 域名的 qps, 5xx 个数，响应时长
其中 `ganglia_conf` 目录是 ganglia 监控脚本

#### 配置 `nginx.conf`

```shell
http {
    ...
    ...

    lua_shared_dict statics_dict    1M; # 初始化变量
    lua_package_path "/etc/nginx/ngx_reqstatus_lua/?.lua";  #路径

    server {
        listen 80;
        server_name  justforfun.com; 

        # 在需要监控的 server_name 添加此句
        log_by_lua_file "/etc/nginx/ngx_reqstatus_lua/hook.lua";
        location /{
            ...
            ...
        }
    }
    # 监控服务
    server {
        listen 127.0.0.1:6080;
        location /{
            access_by_lua_file "/etc/nginx/ngx_reqstatus_lua/status.lua";
        }
    }
}
```

#### 效果

* 查看 `justforfun.com` 的命令

```
curl localhost:6080/?domain=justforfun.com
```

* 输出

```
Server Name:    justforfun.com
Seconds SinceLast:   1.4399998188019 secs
Request Count:      1
Average Req Time:   0 secs
Requests Per Secs:  0.69444453182781
5xx num:    0
```


license
-------

MIT License.

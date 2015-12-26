
## ngx_reqstatus_lua

实时监控 Nginx 域名的 qps, 5xx 个数，响应时长

### 文件注释

```
ganglia_conf/ # ganglia 监控脚本
hook.lua
reqmonit.lua
status.lua
```

### 配置

### nginx.conf

```shell
http {
    ...
    ...

    lua_shared_dict statics_dict    1M; # 初始化变量
    lua_package_path "/etc/nginx/ngx_reqstatus_lua/?.lua";  #路径

    server {
        listen 80;
        server_name  justforfun.com; 

        # 需要在需要监控的servername下面配置
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



### OutPut

```
curl localhost:6080/?domain=justforfun.com
```

```
Server Name:    justforfun.com
Seconds SinceLast:   1.4399998188019 secs
Request Count:      1
Average Req Time:   0 secs
Requests Per Secs:  0.69444453182781
5xx num:    0

```

License
-------

Copyright (c) 2015 by [zheng-ji](http://zheng-ji.info) released under a MIT style license.

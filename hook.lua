-- zheng-ji.info
--
local reqmonit = require("reqmonit")
local request_time = ngx.now() - ngx.req.start_time()
svrname_key = ngx.var.server_name
reqmonit.stat(ngx.shared.statics_dict, svrname_key, request_time)
if tonumber(ngx.var.status) >= 400 then
    reqmonit.stat_5xx(ngx.shared.statics_dict, svrname_key)
end

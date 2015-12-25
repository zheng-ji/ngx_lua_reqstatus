-- zhengji@youmi.net
--
--

local uri_args = ngx.req.get_uri_args()
svrname_key = uri_args["domain"]
if not svrname_key then
    ngx.print("host arg not found.")
    ngx.exit(ngx.HTTP_OK)
end

local reqmonit = require("reqmonit")
local count, avg, total_time, server_err_num = reqmonit.analyse(ngx.shared.statics_dict, svrname_key)
local qps = 0
ngx.say("server name key:\t", svrname_key)
ngx.say("Total seconds since last:\t", total_time, " secs")
ngx.say("Request Count:\t\t", count)
ngx.say("Average req time:\t", avg, " secs")
if total_time > 0 then
    qps = count / total_time
end
ngx.say("Requests per Secs:\t", qps)
ngx.say("5xx num:\t", server_err_num)


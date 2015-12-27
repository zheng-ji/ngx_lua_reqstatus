-- zheng-ji
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
ngx.say("Server Name key:\t", svrname_key)
ngx.say("Seconds SinceLast:\t", total_time)
ngx.say("Average Req Time Sec:\t", avg)
ngx.say("Request Count:\t", count)
if total_time > 0 then
    qps = count / total_time
end
ngx.say("Requests Per Secs:\t", qps)
ngx.say("5xx num:\t", server_err_num)

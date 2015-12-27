-- zheng-ji
--
local reqmoit = {}
local function incr(dict, key, increment)
   increment = increment or 1
   local newval, err = dict:incr(key, increment)
   if err then
      dict:set(key, increment)
      newval = increment
   end
   return newval
end

function reqmoit.stat(dict, key, value)
   local sum_key = key .. "-sum"
   local count_key = key .. "-count"
   local start_time_key = key .. "-start_time"

   local start_time = dict:get(start_time_key)
   if not start_time then
      dict:set(start_time_key, ngx.now())
   end

   local sum = incr(dict, sum_key, value)
   incr(dict, count_key)
end

function reqmoit.stat_5xx(dict, key)
   local server_err_key = key .. "-5xx"
   incr(dict, server_err_key)
end

function reqmoit.analyse(dict, key)
   local sum_key = key .. "-sum"
   local count_key = key .. "-count"
   local start_time_key = key .. "-start_time"
   local server_err_key = key .. "-5xx"

   local elapsed_time = 0
   local avg = 0

   local start_time = dict:get(start_time_key)
   if start_time then
      elapsed_time = ngx.now() - start_time
   end

   local count = dict:get(count_key) or 0
   local sum = dict:get(sum_key) or 0

   if count > 0 then
      avg = sum / count
   end
   local server_err_num = dict:get(server_err_key) or 0

   dict:delete(sum_key)
   dict:delete(start_time_key)
   dict:delete(count_key)
   dict:delete(server_err_key)

   return count, avg, elapsed_time, server_err_num
end

return reqmoit

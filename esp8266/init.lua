function read_analog ()
  r = adc.read(0)
  a = r * 310,3030303 / 1024
  conn=net.createConnection(net.TCP, 0)
  conn:on("receive", function(conn, payload) print(payload) end)
  conn:connect(8000, "172.16.225.106")
  temp = "temp="..a
  loc = "&local=sala-do-servidor"
  var="GET /catcher?"..temp..loc.." HTTP/1.1\r\nHost: 172.16.225.106\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n"
  conn:send(var)
end


     print("Ready to Set up wifi mode")
     wifi.setmode(wifi.STATION)
     gpio.mode(2, gpio.OUTPUT)

     ssid = "GNMK-ADMIN1"
     psw = "g3n3t1c@"
     ip = "172.16.225.190"
     mask = "255.255.255.0"
     gate = "172.16.225.1"
     wifi.sta.config(ssid, psw)
     wifi.sta.setip({ip=ip,netmask=mask,gateway=gate})
     wifi.sta.connect()
     local cnt = 0
     tmr.alarm(3, 1000, 1, function() 
         if (wifi.sta.getip() == nil) and (cnt < 20) then 
         print("Trying Connect to Router, Waiting...")
         cnt = cnt + 1 
         else 
         tmr.stop(3)
         if (cnt < 20) then 
            print("Config done, IP is "..wifi.sta.getip())
            gpio.write(2, gpio.HIGH)
            tmr.alarm(0, 300000, 1, read_analog)      
         else print("Wifi setup time more than 20s, Please verify wifi.sta.config() function. Then re-download the file.")
         end
             cnt = nil;
             collectgarbage();
         end 
          end)


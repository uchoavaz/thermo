function read_analog ()
  r = adc.read(0)
  a = r * 310,3030303 / 1024
  conn=net.createConnection(net.TCP, 0)
  conn:on("receive", function(conn, payload) print(payload) end)
  conn:connect(8005, "172.16.225.18")
  temp = "temp="..a
  var="GET /catcher?"..temp.." HTTP/1.1\r\nHost: 172.16.225.18\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n"
  conn:send(var)
  print(a)
  gpio.write(3, gpio.HIGH)
  gpio.write(3, gpio.LOW)
end


print("Ready to Set up wifi mode")
wifi.setmode(wifi.STATION)
gpio.mode(2, gpio.OUTPUT)
gpio.mode(3, gpio.OUTPUT)
gpio.write(3, gpio.LOW)


ssid = "GNMK-ADMIN1"
psw = "g3n3t1c@"
ip = "172.16.225.190"
mask = "255.255.255.0"
gate = "172.16.225.1"

wifi.sta.config(ssid, psw)
wifi.sta.setip({ip=ip,netmask=mask,gateway=gate})
wifi.sta.connect()
local cnt = 0
tmr.alarm(0, 2000, 1, function()
   if (wifi.sta.status() == 5) then
      print("Config done, IP is "..wifi.sta.getip())
      gpio.write(2, gpio.HIGH)
      tmr.alarm(0, 300000, 1, read_analog)
   else
      print("Trying to connect")
   end
  end)
function read_analog ()
  r = adc.read(0)
  a = r * 310,3030303 / 1024
  conn=net.createConnection(net.TCP, 0)
  conn:on("receive", function(conn, payload) print(payload) end)
  conn:connect(8003, "172.16.225.17")
  temp = "temp="..a
  var="GET /catcher?"..temp.." HTTP/1.1\r\nHost: 172.16.225.17\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n"
  conn:send(var)
  print(a)

end


print("Ready to Set up wifi mode")
wifi.setmode(wifi.STATION)
gpio.mode(0, gpio.OUTPUT)
gpio.mode(1, gpio.OUTPUT)
gpio.write(0, gpio.LOW)
gpio.write(1, gpio.LOW)


ssid = "GNMK-LAB1"
psw = "sc1m0n3g"
ip = "172.16.240.40"
mask = "255.255.255.0"
gate = "172.16.240.1"

wifi.sta.config(ssid, psw)
wifi.sta.setip({ip=ip,netmask=mask,gateway=gate})
wifi.sta.connect()
local cnt = 0
tmr.alarm(0, 2000, 1, function()
   if (wifi.sta.status() == 5) then
      print("Config done, IP is "..wifi.sta.getip())
      gpio.write(0, gpio.HIGH)
      gpio.write(1, gpio.LOW)
      tmr.alarm(0, 300000, 1, read_analog)
   else
      gpio.write(1, gpio.HIGH)
      gpio.write(0, gpio.LOW)
      print("Trying to connect")
   end
  end)

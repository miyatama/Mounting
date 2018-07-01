require "try-cache"

Joushi = {
  stress = 0,
  stressThreshold = 100,
  socket = nil,
}

function Joushi.checkStressLimit(self)
  if self.stress > self.stressThreshold then
    self:dead()
    return true
  else
    return false
  end
end

function Joushi.dead(self)
  print("Hey! I'm dead!")
end

function Joushi.mounting(self)
  try {
    function()
      local socket = require("socket")
      local udp = socket.udp()
      udp:setsockname("127.0.0.1", 0)
      udp:setpeername("127.0.0.1", 1880)
      mountingText = self:getMountingText()
      udp:send(mountingText)

      print('Let\'s mounting!: '..mountingText )
      udp:settimeout(3)
      local data = udp:receive()
      if data == nil then
        print("he denied my conversation...")
      else
        print("now conversation succeed! "..data)
	self.stress = self.stress - 10
      end
      udp:close()
    end,
    catch {
      function(error)
        print(error)  -- raise errro
      end
    }
  }
end

function utf8_from(t)
  local bytearr = {}
  for _, v in ipairs(t) do
    local utf8byte = v < 0 and (0xff + v + 1) or v
    table.insert(bytearr, string.char(utf8byte))
  end
  return table.concat(bytearr)
end

function Joushi.getMountingText(self)
  local r = math.random(7)
  if r == 1 then
    -- when
    return "when are you gonna apologize?"
  elseif r == 2 then
    -- where
    return "where were you yesterday?"
  elseif r == 3 then
    -- who
    return "who do you respect?"
  elseif r == 4 then
    -- what
    return "what takes so much time?"
  elseif r == 5 then
    -- why
    return "why can not you?"
  elseif r == 6 then
    -- how
    return "how much are you?"
  else
    -- direct mounting
    return "hey my dog!"
  end
end

function Joushi.new()
  self = {__index = Joushi}
  o = {}
  return setmetatable(o, self)
end


socket = require("socket")
math.randomseed(os.time())
joushi = Joushi:new()

-- mounting toutine
co = coroutine.create(function()
  local r = math.random(10)
  while true do
    coroutine.yield() 
    if r <= 0 then
      joushi:mounting()
      r = math.random(10)
    else
      r = r - 1
    end
  end
end)

constantStress = coroutine.create(function()
  local r = math.random(2)
  while true do
    coroutine.yield() 
    if r <= 0 then
      joushi.stress = joushi.stress + 10
      r = math.random(2)
    else
      r = r - 1
    end
  end
end)

print('I\'m still alive.')
while true do
  socket.sleep(1)
  coroutine.resume(co)
  coroutine.resume(constantStress)
  if joushi:checkStressLimit() then
    break
  else
    print("joushi stress: "..joushi.stress)
  end
end

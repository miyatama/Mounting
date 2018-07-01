import socket, time, signal, random, threading
from contextlib import closing

stress = 0
deadStressThreshold = 400

class ConstantStress(threading.Thread):
  def __init__(self,interval):
    super(ConstantStress, self).__init__()

    self.interval = interval
    self.lock = threading.Lock()
    self.bStop = False

  def stop(self):
    with self.lock:
      self.bStop = True

  def run(self):
    global stress, deadStressThreshold
    while True:
      with self.lock:
        if self.bStop:
          return
      if stress >= deadStressThreshold:
        print("stress over deadline: {0}".format(stress))
        break
      stress = stress + 10
      time.sleep(self.interval)
    print("constant stress break: {0}".format(stress))

class MountingStress(threading.Thread):
  def __init__(self):
    super(MountingStress, self).__init__()

    self.lock = threading.Lock()
    self.bStop = False

  def stop(self):
    with self.lock:
      self.bStop = True

  def run(self):
    global stress, deadStressThreshold
    host = '127.0.0.1'
    port = 1880
    buffSize = 2046
    while True:
      with self.lock:
        if self.bStop:
          return

      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      with closing(sock):
        sock.settimeout(1.0)
        sock.bind((host, port))
  
        try:
          mountText, addr = sock.recvfrom(buffSize)
          print("Mount: {0}".format(mountText))
          stress += 20
          answer = ""
          if mountText == b"when are you gonna apologize?":
            stress += random.randint(20, 80)
            answer = "sorry, I'm wrong human..."
          elif mountText == b"where were you yesterday?":
            stress += random.randint(20, 80)
            answer = "sorry, was at home..."
          elif mountText == b"who do you respect?":
            stress += random.randint(20, 80)
            answer = "just only you!I'm Happy!"
          elif mountText == b"what takes so much time?":
            stress += random.randint(20, 80)
            answer = "sorry, my ability is missing..."
          elif mountText == b"why can not you?":
            stress += random.randint(20, 80)
            answer = "sorry, my ability is wrong..."
          elif mountText == b"how much are you?":
            stress += random.randint(20, 80)
            answer = "sorry, I am not worth..."
          elif mountText == b"hey my dog!":
            stress += random.randint(20, 80)
            answer = "yes! I'm dog! your dog! I'm Happy!"
          print("Answer: {0}".format(answer)) 
          print(" - mounting stress: {0}".format(stress))
          time.sleep(1)
          sock.sendto(bytes(answer, 'utf-8'), addr)
        except socket.timeout:
          pass
        except:
          # stress -= 5 
          import traceback
          traceback.print_exc()

      if stress < 0:
        stress = 0
      if stress >= deadStressThreshold:
        print("mounting stress break: {0}".format(stress))
        break

def main():
  global stress, deadStressThreshold

  print('I\'m still alive.')
  # constant stress
  constantStress = ConstantStress(1)
  constantStress.start()

  mountingStress = MountingStress()
  mountingStress.start()

  constantStress.join()
  mountingStress.join()
  return

if __name__ == "__main__":
    main()

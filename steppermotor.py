
# importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO
# Importeer de time biblotheek voor tijdfuncties.
from time import sleep
# scheduler
from apscheduler.schedulers.background import BackgroundScheduler
 
# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)
# Stel de GPIO pinnen in voor de stappenmotor:
StepPins = [4,17,27,22]
 
# Set alle pinnen als uitgang.
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
 
# Definieer variabelen.
StepCounter = 0
sched = BackgroundScheduler()
counter = 0
whichway = 0
 
# Voorwaarts
StepCountForward = 8
SeqF = []
SeqF = range(0, StepCountForward)
SeqF[0] = [1,0,0,0]
SeqF[1] = [1,1,0,0]
SeqF[2] = [0,1,0,0]
SeqF[3] = [0,1,1,0]
SeqF[4] = [0,0,1,0]
SeqF[5] = [0,0,1,1]
SeqF[6] = [0,0,0,1]
SeqF[7] = [1,0,0,1]

# Achteruit, gordel om!
StepCountBackward = 8
SeqB = []
SeqB = range(0, StepCountBackward)
SeqB[0] = [1,0,0,1]
SeqB[1] = [0,0,0,1]
SeqB[2] = [0,0,1,1]
SeqB[3] = [0,0,1,0]
SeqB[4] = [0,1,1,0]
SeqB[5] = [0,1,0,0]
SeqB[6] = [1,1,0,0]
SeqB[7] = [1,0,0,0]

Seq = SeqB
StepCount = StepCountBackward
 
try:
  while True:
    # counter += 1
    # print counter

    # # elke X counts, doe iets
    # if counter % 20000 == 0:
    #   if whichway == 0:
    #     Seq = SeqF
    #     StepCount = StepCountForward
    #     whichway = 1
    #   else:
    #     Seq = SeqB
    #     StepCount = StepCountBackward
    #     whichway = 0

    for pin in range(0, 4):
      xpin = StepPins[pin]
      if Seq[StepCounter][pin]!=0:
        print "Stap: %i GPIO Actief: %i" %(StepCounter,xpin)
        GPIO.output(xpin, True)
      else:
        GPIO.output(xpin, False)
 
    StepCounter += 1
 
    # Als we aan het einde van de stappenvolgorde zijn beland start dan opnieuw
    if (StepCounter==StepCount): StepCounter = 0
    if (StepCounter<0): StepCounter = StepCount
 
    # Wacht voor de volgende stap (lager = snellere draaisnelheid)
    sleep(.0001)
 
except KeyboardInterrupt:  
  # GPIO netjes afsluiten
  GPIO.cleanup()
  sched.shutdown()
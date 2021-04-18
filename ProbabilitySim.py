#!/usr/bin/python
# Run x number of sims and return some values

import sys, getopt, math, random, concurrent.futures, time
from datetime import datetime

def main(argv):
	ActivationChance = 0
	CPS = 0
	EffectDuration = 0
	EffectPower = 0
	FightLength = 0
	Iterations = 0
	CoolDown = 0

	opts, args = getopt.getopt(argv,'h', ["ac=", "ActivationChance=", "cps=", "CPS=", "ed=", "EffectDuration=", "cd=", "CoolDown=", "ep=", "EffectPower=", "fl=", "FightLength=", "i=", "Iterations="])
	
	for opt, arg in opts:
		if opt == '-h':
			print('--ac <ActivationChance> --cps <Casts Per Second> --ed <EffectDuration> --cd <CoolDown> --ep <EffectPower> --fl <FightLength> --i <Iterations>')
			sys.exit()
		elif opt in ("--ac", "--ActivationChance"):
			ActivationChance = float(arg)
		elif opt in ("--cps"):
			CPS = float(arg)
		elif opt in ("--ed", "--EffectDuration"):
			EffectDuration = int(arg)
		elif opt in ("--ep", "--EffectPower"):
			EffectPower = int(arg)
		elif opt in ("--fl", "--FightLength"):
			FightLength = int(arg)
		elif opt in ("--i", "--Iterations"):
			Iterations = int(arg)
		elif opt in ("--cd", "--CoolDown"):
			CoolDown = int(arg)

	def Fight(fightNum):
		cast = 1
		active = False
		buffExpiration = 0
		cdExpiration = 0
		activeCasts = 0
		activeEffectTime = 0
		activationInterval = 0.0
		activationCount = 0
		fightTime = 0
		lastActivationIntervalTotal = 0

		while cast <= casts:
			# output a single line for overall progress
			print("Evaluating Fight {0}/{1} cast total {3} with current cast {2}".format(fightCompletedDisplay, Iterations, cast, casts), end="\r")
			# output a line for each cast for debugging. one iteration is recommended
			# print("{5:000.2f} Evaluating Fight {0}/{1} cast {2}/{3} active {4}, activationInterval {6:.2f} activationCount {7}".format(fightCompletedDisplay, Iterations, cast, casts, active, fightTime, activationInterval, activationCount), end="\n")
			
			fightTime = (cast - 1) * castInterval

			if cdExpiration <= fightTime:
				if random.randrange(1, 100) <= math.floor(ActivationChance * 100.0):
					# active effect time will not extend past the fight end
					if fightTime + EffectDuration > 300:	
						activeEffectTime += FightLength - fightTime
					else:
						activeEffectTime += EffectDuration
					active = True						
					buffExpiration = fightTime + EffectDuration
					cdExpiration = fightTime + CoolDown
					activationCount +=  1
					lastActivationIntervalTotal = activationInterval
					# print("Activating. cdExpiraiton {0:.2f}, buffExpiration {1:.2f}".format(cdExpiration, buffExpiration))
				elif cdExpiration < fightTime:
					activationInterval += castInterval
			if buffExpiration < fightTime:
				active = False
			if active:
				activeCasts += 1
			cast += 1
		averageActivationInterval = 0
		if activationCount > 1:
			averageActivationInterval = lastActivationIntervalTotal / activationCount
			# debug post cd interval
			# print("Fight Activation Interval Toatal {0:.2f} with activation count {1} and {2:.2f} seconds of interval at the end for average {3:.2f}".format(activationInterval, activationCount, activationInterval - lastActivationIntervalTotal, averageActivationInterval))
		else:
			averageActivationInterval = lastActivationIntervalTotal
		return activeCasts, activeEffectTime, averageActivationInterval

	fight = 1
	fightCompletedDisplay = 1
	casts = math.floor(float(FightLength) / (1 / CPS))
	castInterval = FightLength / casts
	activeCasts = 0
	activeTime = 0
	startTime = datetime.now(tz=None)
	totalActivationInterval = 0.0

	with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
		futures = []
		while fight <= Iterations: 
			futures.append(executor.submit(Fight, fightNum=fight))
			fight += 1
		for future in concurrent.futures.as_completed(futures):
			fightActiveCasts, fightActiveTime, fightActivationInterval = future.result()
			activeCasts += fightActiveCasts
			activeTime += fightActiveTime
			fightCompletedDisplay += 1
			totalActivationInterval += fightActivationInterval
	
	endTime = datetime.now(tz=None)
	duration = endTime - startTime	
	totalCasts = casts * Iterations
	activeCastRatio = activeCasts / totalCasts
	activeTimeRatio = activeTime / (FightLength * Iterations)
	averageCastPower = EffectPower * activeCastRatio
	averageTimePower = EffectPower * activeTimeRatio

	print("\n\nEvaluation complete after {0}, \nEffect Active on {1:.4f}% of casts and {3:.4f}% of time on average \naverage Effect Power on casts: {2:.4f}\naverage Effect Power on time: {4:.4f}\nActivation Interval post CD: {5:.4f}\n".format(
		"{0}.{1}".format(str(duration).split('.')[0], str(duration).split('.')[1][0:2]), 
		(activeCastRatio * 100.0), 
		averageCastPower, 
		activeTimeRatio * 100.0, 
		averageTimePower, 
		totalActivationInterval / float(Iterations)))

if __name__ == "__main__":
	main(sys.argv[1:])
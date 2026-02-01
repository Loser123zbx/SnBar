
import random

#初始化（不通电）
Light1 = False
Light2 = False

#计数归零
L1Pass = 0
L2Pass = 0
AllPass = 0

times = 10**6

for i in range(times):
    Light1 = random.choice([True, False])
    if Light1 == True:
        L1Pass += 1
        Light2 = random.choice([True, False])
        
        if Light2 == True:
            L2Pass += 1
            AllPass += 1

print(f"total : {times}\nL1Pass : {L1Pass}\nL2Pass : {L2Pass}\nAllPass : {AllPass} ")
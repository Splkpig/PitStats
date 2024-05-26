accountsSplk = ["Splkpig", "Splkion", "NPCBehavior", "SweatySharkBers"]
accountsRey = ["Reyertic", "Rernality", "Gusloverrey"]


def isOwnerAccount(player):
    for ign in accountsSplk:
        if player.lower() == ign.lower():
            return 1
    for ign in accountsRey:
        if player.lower() == ign.lower():
            return 2

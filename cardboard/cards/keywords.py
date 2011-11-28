from cardboard.card import Ability
from cardboard.util import populate

abilities = {}
ability = populate(abilities)


@ability(name="Deathtouch")
def deathtouch(card):
    return Ability.NotImplemented


@ability(name="Defender")
def defender(card):
    card.can_attack = False


@ability(name="Double Strike")
def double_strike(card):
    return Ability.NotImplemented


@ability(name="Enchant")
def enchant(card):
    return Ability.NotImplemented


@ability(name="Equip")
def equip(card):
    return Ability.NotImplemented


@ability(name="First Strike")
def first_strike(card):
    return Ability.NotImplemented


@ability(name="Flash")
def flash(card):
    return Ability.NotImplemented


@ability(name="Flying")
def flying(card):
    return Ability.NotImplemented


@ability(name="Haste")
def haste(card):
    return Ability.NotImplemented


@ability(name="Hexproof")
def hexproof(card):
    return Ability.NotImplemented


@ability(name="Intimidate")
def intimidate(card):
    return Ability.NotImplemented


@ability(name="Landwalk")
def landwalk(card):
    return Ability.NotImplemented


@ability(name="Lifelink")
def lifelink(card):
    return Ability.NotImplemented


@ability(name="Protection")
def protection(card):
    return Ability.NotImplemented


@ability(name="Reach")
def reach(card):
    return Ability.NotImplemented


@ability(name="Shroud")
def shroud(card):
    return Ability.NotImplemented


@ability(name="Trample")
def trample(card):
    return Ability.NotImplemented


@ability(name="Vigilance")
def vigilance(card):
    return Ability.NotImplemented


@ability(name="Banding")
def banding(card):
    return Ability.NotImplemented


@ability(name="Rampage")
def rampage(card):
    return Ability.NotImplemented


@ability(name="Cumulative Upkeep")
def cumulative_upkeep(card):
    return Ability.NotImplemented


@ability(name="Flanking")
def flanking(card):
    return Ability.NotImplemented


@ability(name="Phasing")
def phasing(card):
    return Ability.NotImplemented


@ability(name="Buyback")
def buyback(card):
    return Ability.NotImplemented


@ability(name="Shadow")
def shadow(card):
    return Ability.NotImplemented


@ability(name="Cycling")
def cycling(card):
    return Ability.NotImplemented


@ability(name="Echo")
def echo(card):
    return Ability.NotImplemented


@ability(name="Horsemanship")
def horsemanship(card):
    return Ability.NotImplemented


@ability(name="Fading")
def fading(card):
    return Ability.NotImplemented


@ability(name="Kicker")
def kicker(card):
    return Ability.NotImplemented


@ability(name="Flashback")
def flashback(card):
    return Ability.NotImplemented


@ability(name="Madness")
def madness(card):
    return Ability.NotImplemented


@ability(name="Fear")
def fear(card):
    return Ability.NotImplemented


@ability(name="Morph")
def morph(card):
    return Ability.NotImplemented


@ability(name="Amplify")
def amplify(card):
    return Ability.NotImplemented


@ability(name="Provoke")
def provoke(card):
    return Ability.NotImplemented


@ability(name="Storm")
def storm(card):
    return Ability.NotImplemented


@ability(name="Affinity")
def affinity(card):
    return Ability.NotImplemented


@ability(name="Entwine")
def entwine(card):
    return Ability.NotImplemented


@ability(name="Modular")
def modular(card):
    return Ability.NotImplemented


@ability(name="Sunburst")
def sunburst(card):
    return Ability.NotImplemented


@ability(name="Bushido")
def bushido(card):
    return Ability.NotImplemented


@ability(name="Soulshift")
def soulshift(card):
    return Ability.NotImplemented


@ability(name="Splice")
def splice(card):
    return Ability.NotImplemented


@ability(name="Offering")
def offering(card):
    return Ability.NotImplemented


@ability(name="Ninjutsu")
def ninjutsu(card):
    return Ability.NotImplemented


@ability(name="Epic")
def epic(card):
    return Ability.NotImplemented


@ability(name="Convoke")
def convoke(card):
    return Ability.NotImplemented


@ability(name="Dredge")
def dredge(card):
    return Ability.NotImplemented


@ability(name="Transmute")
def transmute(card):
    return Ability.NotImplemented


@ability(name="Bloodthirst")
def bloodthirst(card):
    return Ability.NotImplemented


@ability(name="Haunt")
def haunt(card):
    return Ability.NotImplemented


@ability(name="Replicate")
def replicate(card):
    return Ability.NotImplemented


@ability(name="Forecast")
def forecast(card):
    return Ability.NotImplemented


@ability(name="Graft")
def graft(card):
    return Ability.NotImplemented


@ability(name="Recover")
def recover(card):
    return Ability.NotImplemented


@ability(name="Ripple")
def ripple(card):
    return Ability.NotImplemented


@ability(name="Split Second")
def split_second(card):
    return Ability.NotImplemented


@ability(name="Suspend")
def suspend(card):
    return Ability.NotImplemented


@ability(name="Vanishing")
def vanishing(card):
    return Ability.NotImplemented


@ability(name="Absorb")
def absorb(card):
    return Ability.NotImplemented


@ability(name="Aura Swap")
def aura_swap(card):
    return Ability.NotImplemented


@ability(name="Delve")
def delve(card):
    return Ability.NotImplemented


@ability(name="Fortify")
def fortify(card):
    return Ability.NotImplemented


@ability(name="Frenzy")
def frenzy(card):
    return Ability.NotImplemented


@ability(name="Gravestorm")
def gravestorm(card):
    return Ability.NotImplemented


@ability(name="Poisonous")
def poisonous(card):
    return Ability.NotImplemented


@ability(name="Transfigure")
def transfigure(card):
    return Ability.NotImplemented


@ability(name="Champion")
def champion(card):
    return Ability.NotImplemented


@ability(name="Changeling")
def changeling(card):
    return Ability.NotImplemented


@ability(name="Evoke")
def evoke(card):
    return Ability.NotImplemented


@ability(name="Hideaway")
def hideaway(card):
    return Ability.NotImplemented


@ability(name="Prowl")
def prowl(card):
    return Ability.NotImplemented


@ability(name="Reinforce")
def reinforce(card):
    return Ability.NotImplemented


@ability(name="Conspire")
def conspire(card):
    return Ability.NotImplemented


@ability(name="Persist")
def persist(card):
    return Ability.NotImplemented


@ability(name="Wither")
def wither(card):
    return Ability.NotImplemented


@ability(name="Retrace")
def retrace(card):
    return Ability.NotImplemented


@ability(name="Devour")
def devour(card):
    return Ability.NotImplemented


@ability(name="Exalted")
def exalted(card):
    return Ability.NotImplemented


@ability(name="Unearth")
def unearth(card):
    return Ability.NotImplemented


@ability(name="Cascade")
def cascade(card):
    return Ability.NotImplemented


@ability(name="Annihilator")
def annihilator(card):
    return Ability.NotImplemented


@ability(name="Level Up")
def level_up(card):
    return Ability.NotImplemented


@ability(name="Rebound")
def rebound(card):
    return Ability.NotImplemented


@ability(name="Totem Armor")
def totem_armor(card):
    return Ability.NotImplemented


@ability(name="Infect")
def infect(card):
    return Ability.NotImplemented


@ability(name="Battle Cry")
def battle_cry(card):
    return Ability.NotImplemented


@ability(name="Living Weapon")
def living_weapon(card):
    return Ability.NotImplemented

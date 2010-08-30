import copy
from datatypes import *

class Sound(Struct):
	def __init__(self, filename=""):
		Struct.__init__(self, "SOUND")
		self.id = Int(0)
		self.filename = String(filename)

class SoundSet(Struct):
	def __init__(self, name="", files=[]):
		Struct.__init__(self, "SOUNDSET")
		self.name = String(name)
		self.sounds = Array(Sound())
		self.last = Int(-1)
		for name in files:
			self.sounds.Add(Sound(name))

class Image(Struct):
	def __init__(self, name="", filename=""):
		Struct.__init__(self, "IMAGE")
		self.name = String(name)
		self.filename = String(filename)
		self.id = Int(-1)
	
class SpriteSet(Struct):
	def __init__(self, name="", image=None, gridx=0, gridy=0):
		Struct.__init__(self, "SPRITESET")
		self.image = Pointer(Image, image) # TODO
		self.gridx = Int(gridx)
		self.gridy = Int(gridy)

class Sprite(Struct):
	def __init__(self, name="", Set=None, x=0, y=0, w=0, h=0):
		Struct.__init__(self, "SPRITE")
		self.name = String(name)
		self.set = Pointer(SpriteSet, Set) # TODO
		self.x = Int(x)
		self.y = Int(y)
		self.w = Int(w)
		self.h = Int(h)

class Pickup(Struct):
	def __init__(self, name="", respawntime=15, spawndelay=0):
		Struct.__init__(self, "PICKUPSPEC")
		self.name = String(name)
		self.respawntime = Int(respawntime)
		self.spawndelay = Int(spawndelay)
		
class SpecialSpec(Struct):
	def __init__(self, name="", respawntime=15, spawndelay=0, duration=30000):
		Struct.__init__(self, "SPECIALSPEC")
		self.name = String(name)
		self.respawntime = Int(respawntime)
		self.spawndelay = Int(spawndelay)
		self.duration = Int(duration)

class AnimKeyframe(Struct):
	def __init__(self, time=0, x=0, y=0, angle=0):
		Struct.__init__(self, "ANIM_KEYFRAME")
		self.time = Float(time)
		self.x = Float(x)
		self.y = Float(y)
		self.angle = Float(angle)

class AnimSequence(Struct):
	def __init__(self):
		Struct.__init__(self, "ANIM_SEQUENCE")
		self.frames = Array(AnimKeyframe())

class Animation(Struct):
	def __init__(self, name=""):
		Struct.__init__(self, "ANIMATION")
		self.name = String(name)
		self.body = AnimSequence()
		self.back_foot = AnimSequence()
		self.front_foot = AnimSequence()
		self.attach = AnimSequence()

class WeaponSpec(Struct):
	def __init__(self, container=None, name=""):
		Struct.__init__(self, "WEAPONSPEC")
		self.name = String(name)
		self.sprite_body = Pointer(Sprite, Sprite())
		self.sprite_cursor = Pointer(Sprite, Sprite())
		self.sprite_proj = Pointer(Sprite, Sprite())
		self.sprite_muzzles = Array(Pointer(Sprite, Sprite()))
		self.visual_size = Int(96)
		
		self.firedelay = Int(500)
		self.maxammo = Int(10)
		self.ammoregentime = Int(0)
		self.damage = Int(1)

		self.offsetx = Float(0)
		self.offsety = Float(0)
		self.muzzleoffsetx = Float(0)
		self.muzzleoffsety = Float(0)
		self.muzzleduration = Float(5)

		# dig out sprites if we have a container
		if container:
			for sprite in container.sprites.items:
				if sprite.name.value == "weapon_"+name+"_body": self.sprite_body.Set(sprite)
				elif sprite.name.value == "weapon_"+name+"_cursor": self.sprite_cursor.Set(sprite)
				elif sprite.name.value == "weapon_"+name+"_proj": self.sprite_proj.Set(sprite)
				elif "weapon_"+name+"_muzzle" in sprite.name.value:
					self.sprite_muzzles.Add(Pointer(Sprite, sprite))

class Weapon_Hammer(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_HAMMER")
		self.base = Pointer(WeaponSpec, WeaponSpec())

class Weapon_Gun(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_GUN")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		self.curvature = Float(1.25)
		self.speed = Float(2200)
		self.lifetime = Float(2.0)
		
class Weapon_Shotgun(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_SHOTGUN")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		self.curvature = Float(1.25)
		self.speed = Float(2200)
		self.speeddiff = Float(0.8)
		self.lifetime = Float(0.25)		

class Weapon_Grenade(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_GRENADE")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		self.curvature = Float(7.0)
		self.speed = Float(1000)
		self.lifetime = Float(2.0)

class Weapon_Rifle(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_RIFLE")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		self.reach = Float(800.0)
		self.bounce_delay = Int(150)
		self.bounce_num = Int(1)
		self.bounce_cost = Float(0)
		
class Weapon_Ninja(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_NINJA")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		self.duration = Int(15000)
		self.movetime = Int(200)
		self.velocity = Int(50)

class Weapon_Hook(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPEC_HOOK")
		self.base = Pointer(WeaponSpec, WeaponSpec())
		
class Weapons(Struct):
	def __init__(self):
		Struct.__init__(self, "WEAPONSPECS")
		self.hammer = Weapon_Hammer()
		self.gun = Weapon_Hammer()
		self.shotgun = Weapon_Shotgun()
		self.grenade = Weapon_Grenade()
		self.rifle = Weapon_Rifle()
		self.ninja = Weapon_Ninja()
		self.hook = Weapon_Hook()
		self.id = Array(WeaponSpec())
		
class SpecialSpec_Nospecial(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_NOSPECIAL")
		self.base = Pointer(SpecialSpec, SpecialSpec())		
		
class SpecialSpec_Megahealth(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_MEGAHEALTH")
		self.base = Pointer(SpecialSpec, SpecialSpec())
		
class SpecialSpec_Yellowarmor(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_YELLOWARMOR")
		self.base = Pointer(SpecialSpec, SpecialSpec())
		
class SpecialSpec_Redarmor(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_REDARMOR")
		self.base = Pointer(SpecialSpec, SpecialSpec())
		
class SpecialSpec_Powersuit(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_POWERSUIT")
		self.base = Pointer(SpecialSpec, SpecialSpec())
	
class SpecialSpec_Ninjapwr(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_NINJAPWR")
		self.base = Pointer(SpecialSpec, SpecialSpec())
		
class SpecialSpec_Hookpwr(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPEC_HOOKPWR")
		self.base = Pointer(SpecialSpec, SpecialSpec())

class SpecialSpec_Reversegravity(Struct):
	def __init__(self):
		Struct.__init__(self,"SPECIALSPEC_REVERSEGRAVITY")
		self.base = Pointer(SpecialSpec, SpecialSpec())
		
class Specials(Struct):
	def __init__(self):
		Struct.__init__(self, "SPECIALSPECS")
		self.nospecial = SpecialSpec_Nospecial()
		self.megahealth = SpecialSpec_Megahealth()
		self.yellowarmor = SpecialSpec_Yellowarmor()
		self.redarmor = SpecialSpec_Redarmor()
		self.powersuit = SpecialSpec_Powersuit()
		self.ninjapwr = SpecialSpec_Ninjapwr()
		self.hookpwr = SpecialSpec_Hookpwr()
		self.reversegravity = SpecialSpec_Reversegravity()
		self.id = Array(SpecialSpec())

class DataContainer(Struct):
	def __init__(self):
		Struct.__init__(self, "DATACONTAINER")
		self.sounds = Array(SoundSet())
		self.images = Array(Image())
		self.pickups = Array(Pickup())
		self.spritesets = Array(SpriteSet())
		self.sprites = Array(Sprite())
		self.animations = Array(Animation())
		self.weapons = Weapons()
		self.specials = Specials()

def FileList(format, num):
	return [format%(x+1) for x in xrange(0,num)]

container = DataContainer()
container.sounds.Add(SoundSet("gun_fire", FileList("audio/wp_gun_fire-%02d.wv", 3)))
container.sounds.Add(SoundSet("shotgun_fire", FileList("audio/wp_shotty_fire-%02d.wv", 3)))

container.sounds.Add(SoundSet("biorifle_fire", FileList("audio/wp_bio_fire-%02d.wv", 3)))
container.sounds.Add(SoundSet("grenade_fire", FileList("audio/wp_flump_launch-%02d.wv", 3)))
container.sounds.Add(SoundSet("hammer_fire", FileList("audio/wp_hammer_swing-%02d.wv", 3)))
container.sounds.Add(SoundSet("hammer_hit", FileList("audio/wp_hammer_hit-%02d.wv", 3)))
container.sounds.Add(SoundSet("ninja_fire", FileList("audio/wp_ninja_attack-%02d.wv", 3)))
container.sounds.Add(SoundSet("spin_impact", FileList("audio/wp_spin_impact-%02d.wv", 3)))
container.sounds.Add(SoundSet("grenade_explode", FileList("audio/wp_flump_explo-%02d.wv", 3)))
container.sounds.Add(SoundSet("bio_explode", FileList("audio/wp_bio_explo-%02d.wv", 3)))
container.sounds.Add(SoundSet("bio_impact", FileList("audio/wp_bio_impact-%02d.wv", 2)))
container.sounds.Add(SoundSet("ninja_hit", FileList("audio/wp_ninja_hit-%02d.wv", 3)))
container.sounds.Add(SoundSet("shaft_fire", FileList("audio/wp_shaft_fire-%02d.wv", 2)))
container.sounds.Add(SoundSet("rifle_fire", FileList("audio/wp_rifle_fire-%02d.wv", 3)))
container.sounds.Add(SoundSet("rifle_bounce", FileList("audio/wp_rifle_bnce-%02d.wv", 3)))
container.sounds.Add(SoundSet("weapon_switch", FileList("audio/wp_switch-%02d.wv", 3)))
container.sounds.Add(SoundSet("gold_attach_player", ["audio/wp_hook_attach.wv"]))

container.sounds.Add(SoundSet("player_pain_short", FileList("audio/vo_teefault_pain_short-%02d.wv", 12)))
container.sounds.Add(SoundSet("player_pain_long", FileList("audio/vo_teefault_pain_long-%02d.wv", 2)))

container.sounds.Add(SoundSet("body_land", FileList("audio/foley_land-%02d.wv", 4)))
container.sounds.Add(SoundSet("player_airjump", FileList("audio/foley_dbljump-%02d.wv", 3)))
container.sounds.Add(SoundSet("player_jump", FileList("audio/foley_foot_left-%02d.wv", 4) +  FileList("audio/foley_foot_right-%02d.wv", 4)))
container.sounds.Add(SoundSet("player_die", FileList("audio/foley_body_splat-%02d.wv", 3)))
container.sounds.Add(SoundSet("player_spawn", FileList("audio/vo_teefault_spawn-%02d.wv", 7)))
container.sounds.Add(SoundSet("player_skid", FileList("audio/sfx_skid-%02d.wv", 4)))
container.sounds.Add(SoundSet("tee_cry", FileList("audio/vo_teefault_cry-%02d.wv", 2)))

container.sounds.Add(SoundSet("hook_loop", FileList("audio/hook_loop-%02d.wv", 2)))

container.sounds.Add(SoundSet("hook_attach_ground", FileList("audio/hook_attach-%02d.wv", 3)))
container.sounds.Add(SoundSet("hook_attach_player", FileList("audio/foley_body_impact-%02d.wv", 3)))
container.sounds.Add(SoundSet("hook_noattach", FileList("audio/hook_noattach-%02d.wv", 2)))
container.sounds.Add(SoundSet("pickup_health", FileList("audio/sfx_pickup_hrt-%02d.wv", 2)))
container.sounds.Add(SoundSet("pickup_armor", FileList("audio/sfx_pickup_arm-%02d.wv", 4)))

container.sounds.Add(SoundSet("pickup_grenade", ["audio/sfx_pickup_launcher.wv"]))
container.sounds.Add(SoundSet("pickup_shotgun", ["audio/sfx_pickup_sg.wv"]))
container.sounds.Add(SoundSet("pickup_ninja", ["audio/sfx_pickup_ninja.wv"]))
container.sounds.Add(SoundSet("pickup_suit", ["audio/sfx_pickup_suit.wv"]))
container.sounds.Add(SoundSet("pickup_gold", ["audio/sfx_pickup_gold.wv"]))
container.sounds.Add(SoundSet("weapon_spawn", FileList("audio/sfx_spawn_wpn-%02d.wv", 3)))
container.sounds.Add(SoundSet("weapon_noammo", FileList("audio/wp_noammo-%02d.wv", 5)))

container.sounds.Add(SoundSet("hit", FileList("audio/sfx_hit_weak-%02d.wv", 2)))

container.sounds.Add(SoundSet("chat_server", ["audio/sfx_msg-server.wv"]))
container.sounds.Add(SoundSet("chat_client", ["audio/sfx_msg-client.wv"]))
container.sounds.Add(SoundSet("ctf_drop", ["audio/sfx_ctf_drop.wv"]))
container.sounds.Add(SoundSet("ctf_return", ["audio/sfx_ctf_rtn.wv"]))
container.sounds.Add(SoundSet("ctf_grab_pl", ["audio/sfx_ctf_grab_pl.wv"]))
container.sounds.Add(SoundSet("ctf_grab_en", ["audio/sfx_ctf_grab_en.wv"]))
container.sounds.Add(SoundSet("ctf_capture", ["audio/sfx_ctf_cap_pl.wv"]))

image_null = Image("null", "")
image_particles = Image("particles", "particles.png")
image_game = Image("game", "game.png")
image_egame = Image("egame", "egame.png")
image_browseicons = Image("browseicons", "browse_icons.png")
image_emoticons = Image("emoticons", "emoticons.png")

container.images.Add(image_null)
container.images.Add(image_game)
container.images.Add(image_egame)
container.images.Add(image_particles)
container.images.Add(Image("cursor", "gui_cursor.png"))
container.images.Add(Image("banner", "gui_logo.png"))
container.images.Add(image_emoticons)
container.images.Add(image_browseicons)
container.images.Add(Image("console_bg", "console.png"))
container.images.Add(Image("console_bar", "console_bar.png"))

container.pickups.Add(Pickup("health"))
container.pickups.Add(Pickup("armor"))
container.pickups.Add(Pickup("weapon"))
container.pickups.Add(Pickup("special", 90, 90))

set_particles = SpriteSet("particles", image_particles, 8, 8)
set_game = SpriteSet("game", image_game, 32, 16)
set_egame = SpriteSet("egame", image_egame, 32, 16)
set_tee = SpriteSet("tee", image_null, 8, 4)
set_browseicons = SpriteSet("browseicons", image_browseicons, 4, 1)
set_emoticons = SpriteSet("emoticons", image_emoticons, 4, 4)

container.spritesets.Add(set_particles)
container.spritesets.Add(set_game)
container.spritesets.Add(set_egame)
container.spritesets.Add(set_tee)
container.spritesets.Add(set_browseicons)
container.spritesets.Add(set_emoticons)

container.sprites.Add(Sprite("part_slice", set_particles, 0,0,1,1))
container.sprites.Add(Sprite("part_ball", set_particles, 1,0,1,1))
container.sprites.Add(Sprite("part_splat01", set_particles, 2,0,1,1))
container.sprites.Add(Sprite("part_splat02", set_particles, 3,0,1,1))
container.sprites.Add(Sprite("part_splat03", set_particles, 4,0,1,1))

container.sprites.Add(Sprite("part_smoke", set_particles, 0,1,1,1))
container.sprites.Add(Sprite("part_shell", set_particles, 0,2,2,2))
container.sprites.Add(Sprite("part_expl01", set_particles, 0,4,4,4))
container.sprites.Add(Sprite("part_airjump", set_particles, 2,2,2,2))

container.sprites.Add(Sprite("health_overfill", set_egame, 10,0,2,2))
container.sprites.Add(Sprite("health_full", set_game, 21,0,2,2))
container.sprites.Add(Sprite("health_empty", set_game, 23,0,2,2))
container.sprites.Add(Sprite("armor_overfill", set_egame, 10,2,2,2))
container.sprites.Add(Sprite("armor_full", set_game, 21,2,2,2))
container.sprites.Add(Sprite("armor_empty", set_game, 23,2,2,2))

container.sprites.Add(Sprite("star1", set_game, 15,0,2,2))
container.sprites.Add(Sprite("star2", set_game, 17,0,2,2))
container.sprites.Add(Sprite("star3", set_game, 19,0,2,2))
	
container.sprites.Add(Sprite("part1", set_game, 6,0,1,1))
container.sprites.Add(Sprite("part2", set_game, 6,1,1,1))
container.sprites.Add(Sprite("part3", set_game, 7,0,1,1))
container.sprites.Add(Sprite("part4", set_game, 7,1,1,1))
container.sprites.Add(Sprite("part5", set_game, 8,0,1,1))
container.sprites.Add(Sprite("part6", set_game, 8,1,1,1))
container.sprites.Add(Sprite("part7", set_game, 9,0,2,2))
container.sprites.Add(Sprite("part8", set_game, 11,0,2,2))
container.sprites.Add(Sprite("part9", set_game, 13,0,2,2))

container.sprites.Add(Sprite("weapon_gun_body", set_game, 2,4,4,2))
container.sprites.Add(Sprite("weapon_gun_cursor", set_game, 0,4,2,2))
container.sprites.Add(Sprite("weapon_gun_proj", set_game, 6,4,2,2))
container.sprites.Add(Sprite("weapon_gun_muzzle1", set_game, 8,4,3,2))
container.sprites.Add(Sprite("weapon_gun_muzzle2", set_game, 12,4,3,2))
container.sprites.Add(Sprite("weapon_gun_muzzle3", set_game, 16,4,3,2))

container.sprites.Add(Sprite("weapon_shotgun_body", set_game, 2,6,8,2))
container.sprites.Add(Sprite("weapon_shotgun_cursor", set_game, 0,6,2,2))
container.sprites.Add(Sprite("weapon_shotgun_proj", set_game, 10,6,2,2))
container.sprites.Add(Sprite("weapon_shotgun_muzzle1", set_game, 12,6,3,2))
container.sprites.Add(Sprite("weapon_shotgun_muzzle2", set_game, 16,6,3,2))
container.sprites.Add(Sprite("weapon_shotgun_muzzle3", set_game, 20,6,3,2))

container.sprites.Add(Sprite("weapon_grenade_body", set_game, 2,8,7,2))
container.sprites.Add(Sprite("weapon_grenade_cursor", set_game, 0,8,2,2))
container.sprites.Add(Sprite("weapon_grenade_proj", set_game, 10,8,2,2))

container.sprites.Add(Sprite("weapon_hammer_body", set_game, 2,1,4,3))
container.sprites.Add(Sprite("weapon_hammer_cursor", set_game, 0,0,2,2))
container.sprites.Add(Sprite("weapon_hammer_proj", set_game, 0,0,0,0))

container.sprites.Add(Sprite("weapon_ninja_body", set_game, 2,10,7,2))
container.sprites.Add(Sprite("weapon_ninja_cursor", set_game, 0,10,2,2))
container.sprites.Add(Sprite("weapon_ninja_proj", set_game, 0,0,0,0))

container.sprites.Add(Sprite("weapon_rifle_body", set_game, 2,12,7,3))
container.sprites.Add(Sprite("weapon_rifle_cursor", set_game, 0,12,2,2))
container.sprites.Add(Sprite("weapon_rifle_proj", set_game, 10,12,2,2))

container.sprites.Add(Sprite("weapon_hook_body", set_egame, 13,0,2,1))
container.sprites.Add(Sprite("weapon_hook_cursor", set_game, 3,0,2,1))
container.sprites.Add(Sprite("weapon_hook_proj", set_game, 3,0,2,1))

container.sprites.Add(Sprite("weapon_shaft_body", set_egame, 2,0,7,4))
container.sprites.Add(Sprite("weapon_shaft_cursor", set_egame, 0,1,2,2))
container.sprites.Add(Sprite("weapon_shaft_proj", set_egame, 0,0,1,1))

container.sprites.Add(Sprite("weapon_spingun_body", set_egame, 2,4,7,3))
container.sprites.Add(Sprite("weapon_spingun_cursor", set_egame, 0,3,2,2))
container.sprites.Add(Sprite("weapon_spingun_proj", set_egame, 10,4,2,2))
container.sprites.Add(Sprite("weapon_spingun_vortex", set_egame, 19,0,4,4))
container.sprites.Add(Sprite("weapon_spingun_lightning1", set_egame, 23,0,2,4))
container.sprites.Add(Sprite("weapon_spingun_lightning2", set_egame, 25,0,2,4))
container.sprites.Add(Sprite("weapon_spingun_halo", set_egame, 27,0,4,4))

container.sprites.Add(Sprite("weapon_biorifle_body", set_egame, 2,7,7,3))
container.sprites.Add(Sprite("weapon_biorifle_cursor", set_egame, 0,5,2,2))
container.sprites.Add(Sprite("weapon_biorifle_proj", set_egame, 0,7,2,2))
container.sprites.Add(Sprite("weapon_biorifle_sticky1", set_egame, 0,9,2,2))
container.sprites.Add(Sprite("weapon_biorifle_sticky2", set_egame, 0,11,2,2))
container.sprites.Add(Sprite("weapon_biorifle_splash", set_egame, 0,13,2,2))

container.sprites.Add(Sprite("shaft_end1", set_egame, 13,2,2,2))
container.sprites.Add(Sprite("shaft_end2", set_egame, 15,2,2,2))
container.sprites.Add(Sprite("shaft_end3", set_egame, 17,2,2,2))
container.sprites.Add(Sprite("shaft_beam1", set_egame, 13,4,7,2))

container.sprites.Add(Sprite("hook_chain", set_game, 2,0,1,1))
container.sprites.Add(Sprite("hook_head", set_game, 3,0,2,1))

container.sprites.Add(Sprite("hook_powerup_chain", set_egame, 13,0,1,1))
container.sprites.Add(Sprite("hook_powerup_head", set_egame, 14,0,2,1))

container.sprites.Add(Sprite("weapon_ninja_muzzle1", set_game, 25,0,7,4))
container.sprites.Add(Sprite("weapon_ninja_muzzle2", set_game, 25,4,7,4))
container.sprites.Add(Sprite("weapon_ninja_muzzle3", set_game, 25,8,7,4))

container.sprites.Add(Sprite("pickup_health", set_game, 10,2,2,2))
container.sprites.Add(Sprite("pickup_armor", set_game, 12,2,2,2))
container.sprites.Add(Sprite("pickup_weapon", set_game, 3,0,6,2))
container.sprites.Add(Sprite("pickup_ninja", set_game, 3,10,7,2))
container.sprites.Add(Sprite("pickup_hook", set_egame, 9,6,2,3))
container.sprites.Add(Sprite("pickup_suit", set_egame, 11,6,3,3))

container.sprites.Add(Sprite("flag_blue", set_game, 12,8,4,8))
container.sprites.Add(Sprite("flag_red", set_game, 16,8,4,8))

container.sprites.Add(Sprite("tee_body", set_tee, 0,0,3,3))
container.sprites.Add(Sprite("tee_body_outline", set_tee, 3,0,3,3))
container.sprites.Add(Sprite("tee_foot", set_tee, 6,1,2,1))
container.sprites.Add(Sprite("tee_foot_outline", set_tee, 6,2,2,1))
container.sprites.Add(Sprite("tee_hand", set_tee, 6,0,1,1))
container.sprites.Add(Sprite("tee_hand_outline", set_tee, 7,0,1,1))
container.sprites.Add(Sprite("tee_eye_normal", set_tee, 2,3,1,1))
container.sprites.Add(Sprite("tee_eye_angry", set_tee, 3,3,1,1))
container.sprites.Add(Sprite("tee_eye_pain", set_tee, 4,3,1,1))
container.sprites.Add(Sprite("tee_eye_happy", set_tee, 5,3,1,1))
container.sprites.Add(Sprite("tee_eye_dead", set_tee, 6,3,1,1))
container.sprites.Add(Sprite("tee_eye_surprise", set_tee, 7,3,1,1))

container.sprites.Add(Sprite("oop", set_emoticons, 0, 0, 1, 1))
container.sprites.Add(Sprite("exclamation", set_emoticons, 1, 0, 1, 1))
container.sprites.Add(Sprite("hearts", set_emoticons, 2, 0, 1, 1))
container.sprites.Add(Sprite("drop", set_emoticons, 3, 0, 1, 1))
container.sprites.Add(Sprite("dotdot", set_emoticons, 0, 1, 1, 1))
container.sprites.Add(Sprite("music1", set_emoticons, 1, 1, 1, 1))
container.sprites.Add(Sprite("music2", set_emoticons, 2, 1, 1, 1))
container.sprites.Add(Sprite("ghost", set_emoticons, 3, 1, 1, 1))
container.sprites.Add(Sprite("sushi", set_emoticons, 0, 2, 1, 1))
container.sprites.Add(Sprite("splattee", set_emoticons, 1, 2, 1, 1))
container.sprites.Add(Sprite("deviltee", set_emoticons, 2, 2, 1, 1))
container.sprites.Add(Sprite("zomg", set_emoticons, 3, 2, 1, 1))
container.sprites.Add(Sprite("zzz", set_emoticons, 0, 3, 1, 1))
container.sprites.Add(Sprite("blank1", set_emoticons, 1, 3, 1, 1))
container.sprites.Add(Sprite("deadtee", set_emoticons, 2, 3, 1, 1))
container.sprites.Add(Sprite("blank2", set_emoticons, 3, 3, 1, 1))


container.sprites.Add(Sprite("browse_lock", set_browseicons, 0,0,1,1))
container.sprites.Add(Sprite("browse_heart", set_browseicons, 1,0,1,1))
container.sprites.Add(Sprite("browse_unpure", set_browseicons, 3,0,1,1))

anim = Animation("base")
anim.body.frames.Add(AnimKeyframe(0, 0, -4, 0))
anim.back_foot.frames.Add(AnimKeyframe(0, 0, 10, 0))
anim.front_foot.frames.Add(AnimKeyframe(0, 0, 10, 0))
container.animations.Add(anim)

anim = Animation("idle")
anim.back_foot.frames.Add(AnimKeyframe(0, -7, 0, 0))
anim.front_foot.frames.Add(AnimKeyframe(0, 7, 0, 0))
container.animations.Add(anim)

anim = Animation("inair")
anim.back_foot.frames.Add(AnimKeyframe(0, -3, 0, -0.1))
anim.front_foot.frames.Add(AnimKeyframe(0, 3, 0, -0.1))
container.animations.Add(anim)

anim = Animation("walk")
anim.body.frames.Add(AnimKeyframe(0.0, 0, 0, 0))
anim.body.frames.Add(AnimKeyframe(0.2, 0,-1, 0))
anim.body.frames.Add(AnimKeyframe(0.4, 0, 0, 0))
anim.body.frames.Add(AnimKeyframe(0.6, 0, 0, 0))
anim.body.frames.Add(AnimKeyframe(0.8, 0,-1, 0))
anim.body.frames.Add(AnimKeyframe(1.0, 0, 0, 0))

anim.back_foot.frames.Add(AnimKeyframe(0.0,  8, 0, 0))
anim.back_foot.frames.Add(AnimKeyframe(0.2, -8, 0, 0))
anim.back_foot.frames.Add(AnimKeyframe(0.4,-10,-4, 0.2))
anim.back_foot.frames.Add(AnimKeyframe(0.6, -8,-8, 0.3))
anim.back_foot.frames.Add(AnimKeyframe(0.8,  4,-4,-0.2))
anim.back_foot.frames.Add(AnimKeyframe(1.0,  8, 0, 0))

anim.front_foot.frames.Add(AnimKeyframe(0.0,-10,-4, 0.2))
anim.front_foot.frames.Add(AnimKeyframe(0.2, -8,-8, 0.3))
anim.front_foot.frames.Add(AnimKeyframe(0.4,  4,-4,-0.2))
anim.front_foot.frames.Add(AnimKeyframe(0.6,  8, 0, 0))
anim.front_foot.frames.Add(AnimKeyframe(0.8,  8, 0, 0))
anim.front_foot.frames.Add(AnimKeyframe(1.0,-10,-4, 0.2))
container.animations.Add(anim)

anim = Animation("hammer_swing")
anim.attach.frames.Add(AnimKeyframe(0.0, 0, 0, -0.10))
anim.attach.frames.Add(AnimKeyframe(0.3, 0, 0,  0.25))
anim.attach.frames.Add(AnimKeyframe(0.4, 0, 0,  0.30))
anim.attach.frames.Add(AnimKeyframe(0.5, 0, 0,  0.25))
anim.attach.frames.Add(AnimKeyframe(1.0, 0, 0, -0.10))
container.animations.Add(anim)
			
anim = Animation("ninja_swing")
anim.attach.frames.Add(AnimKeyframe(0.00, 0, 0, -0.25))
anim.attach.frames.Add(AnimKeyframe(0.10, 0, 0, -0.05))
anim.attach.frames.Add(AnimKeyframe(0.15, 0, 0,  0.35))
anim.attach.frames.Add(AnimKeyframe(0.42, 0, 0,  0.40))
anim.attach.frames.Add(AnimKeyframe(0.50, 0, 0,  0.35))
anim.attach.frames.Add(AnimKeyframe(1.00, 0, 0, -0.25))
container.animations.Add(anim)

weapon = WeaponSpec(container, "hammer")
weapon.firedelay.Set(125)
weapon.damage.Set(3)
weapon.visual_size.Set(96)
weapon.offsetx.Set(4)
weapon.offsety.Set(-20)
container.weapons.hammer.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "gun")
weapon.firedelay.Set(125)
weapon.ammoregentime.Set(500)
weapon.visual_size.Set(64)
weapon.offsetx.Set(32)
weapon.offsety.Set(-4)
weapon.muzzleoffsetx.Set(50)
weapon.muzzleoffsety.Set(6)
container.weapons.gun.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "shotgun")
weapon.firedelay.Set(500)
weapon.visual_size.Set(96)
weapon.offsetx.Set(24)
weapon.offsety.Set(-2)
weapon.muzzleoffsetx.Set(70)
weapon.muzzleoffsety.Set(6)
container.weapons.shotgun.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "grenade")
weapon.firedelay.Set(500) # TODO: fix this
weapon.visual_size.Set(96)
weapon.offsetx.Set(24)
weapon.offsety.Set(-2)
container.weapons.grenade.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "rifle")
weapon.firedelay.Set(800)
weapon.visual_size.Set(92)
weapon.damage.Set(5)
weapon.offsetx.Set(24)
weapon.offsety.Set(-2)
container.weapons.rifle.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "ninja")
weapon.firedelay.Set(800)
weapon.damage.Set(9)
weapon.visual_size.Set(96)
weapon.offsetx.Set(0)
weapon.offsety.Set(0)
weapon.muzzleoffsetx.Set(40)
weapon.muzzleoffsety.Set(-4)
container.weapons.ninja.base.Set(weapon)
container.weapons.id.Add(weapon)

weapon = WeaponSpec(container, "hook")
weapon.firedelay.Set(10)
weapon.damage.Set(0)
weapon.visual_size.Set(0)
weapon.offsetx.Set(0)
weapon.offsety.Set(0)
weapon.muzzleoffsetx.Set(0)
weapon.muzzleoffsety.Set(0)
container.weapons.hook.base.Set(weapon)
container.weapons.id.Add(weapon)

# container.specials.id.Add(SpecialSpec("nospecial", 0, 0))
# container.specials.id.Add(SpecialSpec("megahealth", 35, 10, 0))
# container.specials.id.Add(SpecialSpec("yellowarmor", 25, 1, 0))
# container.specials.id.Add(SpecialSpec("redarmor", 25, 1, 0))
# container.specials.id.Add(SpecialSpec("powersuit", 90, 30))
# container.specials.id.Add(SpecialSpec("ninjapwr", 45, 30))
# container.specials.id.Add(SpecialSpec("hookpwr", 90, 30))
# container.specials.id.Add(SpecialSpec("reversegravity", 90, 30))

special = SpecialSpec("nospecial", 0, 0)
container.specials.nospecial.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("megahealth", 35, 10)
container.specials.megahealth.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("yellowarmor", 25, 1)
container.specials.yellowarmor.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("redarmor", 25, 1)
container.specials.redarmor.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("powersuit", 30, 10)
container.specials.powersuit.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("ninjapwr", 30, 15)
container.specials.ninjapwr.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("hookpwr", 90, 45)
container.specials.hookpwr.base.Set(special)
container.specials.id.Add(special)

special = SpecialSpec("reversegravity", 90, 45)
container.specials.reversegravity.base.Set(special)
container.specials.id.Add(special)
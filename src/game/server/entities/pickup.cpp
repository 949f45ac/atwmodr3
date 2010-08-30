#include <game/generated/protocol.h>
#include <game/server/gamecontext.h>
#include "pickup.h"

CPickup::CPickup(CGameWorld *pGameWorld, int Type, int SubType)
: CEntity(pGameWorld, NETOBJTYPE_PICKUP)
{
	m_Type = Type;
	m_Subtype = SubType;
	m_ProximityRadius = PickupPhysSize;

	Reset();
	
	GameWorld()->InsertEntity(this);
}

void CPickup::Reset()
{
	if (m_Type != POWERUP_SPECIAL)
	{	
		if (g_pData->m_aPickups[m_Type].m_Spawndelay > 0)
			m_SpawnTick = Server()->Tick() + Server()->TickSpeed() * g_pData->m_aPickups[m_Type].m_Spawndelay;
		else
			m_SpawnTick = -1;
	}
	else
	{
		if (g_pData->m_Specials.m_aId[m_Subtype].m_Spawndelay > 0)
			m_SpawnTick = Server()->Tick() + Server()->TickSpeed() * g_pData->m_Specials.m_aId[m_Subtype].m_Spawndelay;
		else
			m_SpawnTick = -1;
	}
}

void CPickup::Tick()
{
	// wait for respawn
	if(m_SpawnTick > 0)
	{
		if(Server()->Tick() > m_SpawnTick)
		{
			// respawn
			m_SpawnTick = -1;

			if(m_Type == POWERUP_WEAPON)
				GameServer()->CreateSound(m_Pos, SOUND_WEAPON_SPAWN);
		}
		else
			return;
	}
	// Check if a player intersected us
	CCharacter *pChr = GameServer()->m_World.ClosestCharacter(m_Pos, 20.0f, 0);
	if(pChr && pChr->IsAlive())
	{
		// player picked us up, is someone was hooking us, let them go
		int RespawnTime = -1;
		switch (m_Type)
		{
			case POWERUP_HEALTH:
				if(pChr->IncreaseHealth(1))
				{
					GameServer()->CreateSound(m_Pos, SOUND_PICKUP_HEALTH);
					RespawnTime = g_pData->m_aPickups[m_Type].m_Respawntime;
				}
				break;
				
			case POWERUP_ARMOR:
				if(pChr->IncreaseArmor(1))
				{
					GameServer()->CreateSound(m_Pos, SOUND_PICKUP_ARMOR);
					RespawnTime = g_pData->m_aPickups[m_Type].m_Respawntime;
				}
				break;

			case POWERUP_WEAPON:
				if(m_Subtype >= 0 && m_Subtype < NUM_WEAPONS)
				{
					if(pChr->GiveWeapon(m_Subtype, 10))
					{
						RespawnTime = g_pData->m_aPickups[m_Type].m_Respawntime;

						if(m_Subtype == WEAPON_GRENADE)
							GameServer()->CreateSound(m_Pos, SOUND_PICKUP_GRENADE);
						else if(m_Subtype == WEAPON_SHOTGUN)
							GameServer()->CreateSound(m_Pos, SOUND_PICKUP_SHOTGUN);
						else if(m_Subtype == WEAPON_RIFLE)
							GameServer()->CreateSound(m_Pos, SOUND_PICKUP_SHOTGUN);

						if(pChr->GetPlayer())
							GameServer()->SendWeaponPickup(pChr->GetPlayer()->GetCID(), m_Subtype);
					}
				}
				break;
				
			case POWERUP_SPECIAL:
			{
				if(m_Subtype >= 0 && m_Subtype < NUM_SPECIALS)
 				{
					if(pChr->GiveSpecial(m_Subtype))
					{
						RespawnTime = g_pData->m_Specials.m_aId[m_Subtype].m_Respawntime;
						
						if(m_Subtype == SPECIAL_POWERSUIT)
							GameServer()->CreateSound(m_Pos, SOUND_PICKUP_SUIT);
						if(m_Subtype == SPECIAL_HOOKPWR)
							GameServer()->CreateSound(m_Pos, SOUND_PICKUP_GOLD);
					}
				}
			
			break;
			}
				
			default:
			break;
		};

		if(RespawnTime >= 0)
		{
			dbg_msg("game", "pickup player='%d:%s' item=%d/%d",
				pChr->GetPlayer()->GetCID(), Server()->ClientName(pChr->GetPlayer()->GetCID()), m_Type, m_Subtype);
			m_SpawnTick = Server()->Tick() + Server()->TickSpeed() * RespawnTime;
		}
	}
}

void CPickup::Snap(int SnappingClient)
{
	if(m_SpawnTick != -1 || NetworkClipped(SnappingClient))
		return;

	CNetObj_Pickup *pP = static_cast<CNetObj_Pickup *>(Server()->SnapNewItem(NETOBJTYPE_PICKUP, m_Id, sizeof(CNetObj_Pickup)));
	pP->m_X = (int)m_Pos.x;
	pP->m_Y = (int)m_Pos.y;
	pP->m_Type = m_Type;
	pP->m_Subtype = m_Subtype;
}

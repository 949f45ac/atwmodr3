#ifndef GAME_CLIENT_COMPONENTS_EFFECTS_H
#define GAME_CLIENT_COMPONENTS_EFFECTS_H
#include <game/client/component.h>

class CEffects : public CComponent
{	
	bool m_Add50hz;
	bool m_Add100hz;
public:
	CEffects();

	virtual void OnRender();

	void BulletTrail(vec2 Pos);
	void SmokeTrail(vec2 Pos, vec2 Vel);
	void SkidTrail(vec2 Pos, vec2 Vel);
	void Explosion(vec2 Pos);
	void HammerHit(vec2 Pos);
	void AirJump(vec2 Pos);
	void DamageIndicator(vec2 Pos, vec2 Dir);
	void PlayerSpawn(vec2 Pos);
	void PlayerDeath(vec2 Pos, int ClientId);
	void PowerupShine(vec2 Pos, vec2 Size);

	void Update();
};
#endif

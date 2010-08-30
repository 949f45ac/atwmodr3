#ifndef GAME_GAMECORE_H
#define GAME_GAMECORE_H

#include <base/system.h>
#include <base/math.h>

#include <math.h>
#include "collision.h"
#include <engine/shared/protocol.h>
#include <game/generated/protocol.h>


class CTuneParam
{
	int m_Value;
public:
	void Set(int v) { m_Value = v; }
	int Get() const { return m_Value; }
	CTuneParam &operator = (int v) { m_Value = (int)(v*100.0f); return *this; }
	CTuneParam &operator = (float v) { m_Value = (int)(v*100.0f); return *this; }
	operator float() const { return m_Value/100.0f; }
};

class CTuningParams
{
public:
	CTuningParams()
	{
		const float TicksPerSecond = 50.0f;
		#define MACRO_TUNING_PARAM(Name,ScriptName,Value) m_##Name.Set((int)(Value*100.0f));
		#include "tuning.h"
		#undef MACRO_TUNING_PARAM
	}

	static const char *m_apNames[];
	
	#define MACRO_TUNING_PARAM(Name,ScriptName,Value) CTuneParam m_##Name;
	#include "tuning.h"
	#undef MACRO_TUNING_PARAM
	
	static int Num() { return sizeof(CTuningParams)/sizeof(int); }
	bool Set(int Index, float Value);
	bool Set(const char *pName, float Value);
	bool Get(int Index, float *pValue);
	bool Get(const char *pName, float *pValue);
};


inline vec2 GetDirection(int Angle)
{
	float a = Angle/256.0f;
	return vec2(cosf(a), sinf(a));
}

inline vec2 GetDir(float a)
{
	return vec2(cosf(a), sinf(a));
}

inline float GetAngle(vec2 Dir)
{
	if(Dir.x == 0 && Dir.y == 0)
		return 0.0f;
	float a = atanf(Dir.y/Dir.x);
	if(Dir.x < 0)
		a = a+pi;
	return a;
}

inline void StrToInts(int *pInts, int Num, const char *pStr)
{
	int Index = 0;
	while(Num)
	{
		char aBuf[4] = {0,0,0,0};
		for(int c = 0; c < 4 && pStr[Index]; c++, Index++)
			aBuf[c] = pStr[Index];
		*pInts = ((aBuf[0]+128)<<24)|((aBuf[1]+128)<<16)|((aBuf[2]+128)<<8)|(aBuf[3]+128);
		pInts++;
		Num--;
	}
	
	// null terminate
	pInts[-1] &= 0xffffff00;
}

inline void IntsToStr(const int *pInts, int Num, char *pStr)
{
	while(Num)
	{
		pStr[0] = (((*pInts)>>24)&0xff)-128;
		pStr[1] = (((*pInts)>>16)&0xff)-128;
		pStr[2] = (((*pInts)>>8)&0xff)-128;
		pStr[3] = ((*pInts)&0xff)-128;
		pStr += 4;
		pInts++;
		Num--;
	}
	
	// null terminate
	pStr[-1] = 0;
}



inline vec2 CalcPos(vec2 p, vec2 v, float Curvature, float Speed, float t)
{
	vec2 n;
	t *= Speed;
	n.x = p.x + v.x*t;
	n.y = p.y + v.y*t + Curvature/10000*(t*t);
	return n;
}


template<typename T>
inline T SaturatedAdd(T Min, T Max, T Current, T Modifier)
{
	if(Modifier < 0)
	{
		if(Current < Min)
			return Current;
		Current += Modifier;
		if(Current < Min)
			Current = Min;
		return Current;
	}
	else
	{
		if(Current > Max)
			return Current;
		Current += Modifier;
		if(Current > Max)
			Current = Max;
		return Current;
	}
}


float VelocityRamp(float Value, float Start, float Range, float Curvature);

// hooking stuff
enum
{
	HOOK_RETRACTED=-1,
	HOOK_IDLE=0,
	HOOK_RETRACT_START=1,
	HOOK_RETRACT_END=3,
	HOOK_FLYING,
	HOOK_GRABBED,
	
	COREEVENT_GROUND_JUMP=0x01,
	COREEVENT_AIR_JUMP=0x02,
	COREEVENT_HOOK_LAUNCH=0x04,
	COREEVENT_HOOK_ATTACH_PLAYER=0x08,
	COREEVENT_HOOK_ATTACH_GROUND=0x10,
	COREEVENT_HOOK_HIT_NOHOOK=0x20,
	COREEVENT_HOOK_RETRACT=0x40,
};

class CWorldCore
{
public:
	CWorldCore()
	{
		mem_zero(m_apCharacters, sizeof(m_apCharacters));
	}
	
	CTuningParams m_Tuning;
	class CCharacterCore *m_apCharacters[MAX_CLIENTS];
};

class CCharacterCore
{
	CWorldCore *m_pWorld;
	CCollision *m_pCollision;
public:
	vec2 m_Pos;
	vec2 m_Vel;
	
	vec2 m_HookPos;
	vec2 m_HookDir;
	int m_HookTick;
	int m_HookState;
	int m_HookedPlayer;
	
	bool m_HookPower;
	bool m_Suit;
	bool m_ReverseGravity;
	
	int m_HookDecaytick;
	int m_SuitDecaytick;
	int m_GravityDecaytick;
	
	int m_HookpwrDuration;
	int m_SuitDuration;
	int m_GravityDuration;
	
	int m_Jumped;
	
	int m_Direction;
	int m_Angle;
	CNetObj_PlayerInput m_Input;
	
	int m_TriggeredEvents;
	
	void Init(CWorldCore *pWorld, CCollision *pCollision);
	void Reset();
	void Tick(bool UseInput);
	void Move();
	void CCharacterCore::EnableSpecial(int Type, int Duration);
	
	void Read(const CNetObj_CharacterCore *pObjCore);
	void Write(CNetObj_CharacterCore *pObjCore);
	void Quantize();
};

#endif
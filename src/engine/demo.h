#ifndef ENGINE_DEMO_H
#define ENGINE_DEMO_H

#include "kernel.h"

class IDemoPlayer : public IInterface
{
	MACRO_INTERFACE("demoplayer", 0)
public:
	class CInfo
	{
	public:
		bool m_Paused;
		float m_Speed;

		int m_FirstTick;
		int m_CurrentTick;
		int m_LastTick;
	};

	~IDemoPlayer() {}
	virtual void SetSpeed(float Speed) = 0;
	virtual int SetPos(float Precent) = 0;
	virtual void Pause() = 0;
	virtual void Unpause() = 0;
	virtual const CInfo *BaseInfo() const = 0;
};

#endif

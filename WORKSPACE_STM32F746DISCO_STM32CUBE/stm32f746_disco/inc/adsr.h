

//#include "notes.h"

#define ATTACK_DURATION  1000.0
#define RELEASE_DURATION 1000.0
enum state_t  { INIT, NOTE_OFF, ATTACK, DECAY, SUSTAIN, RELEASE };


struct adsr_TypeStruct
{

};

int adsr(struct adsr_TypeStruct* );

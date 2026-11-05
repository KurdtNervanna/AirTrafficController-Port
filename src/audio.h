#ifndef ATC_AUDIO_H
#define ATC_AUDIO_H
int  audio_init(int rate);                         /* 8-bit unsigned mono; 0 if unavailable */
void audio_push(const unsigned char *s, int n);    /* queue samples (emulation thread)      */
void audio_service(void);                          /* refill waveOut buffers                */
void audio_shutdown(void);
#endif

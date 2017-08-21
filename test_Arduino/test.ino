#include <MozziGuts.h>
#include <ReverbTank.h>
#include <Line.h> // for smooth transitions
#include <Oscil.h> // oscillator template
#include <tables/triangle_warm8192_int8.h> // triangle table for oscillator
#include <tables/cos8192_int8.h>
#include <tables/envelop2048_uint8.h>
#include <mozzi_midi.h>

#define CONTROL_RATE 512 //64 // powers of 2 please

// use: Oscil <table_size, update_rate> oscilName (wavetable), look in .h file of table #included above
Oscil <TRIANGLE_WARM8192_NUM_CELLS, AUDIO_RATE> aTriangle(TRIANGLE_WARM8192_DATA);
// Synth from PhaseMod_Envelope example
Oscil <COS8192_NUM_CELLS, AUDIO_RATE> aCarrier(COS8192_DATA);
Oscil <COS8192_NUM_CELLS, AUDIO_RATE> aModulator(COS8192_DATA);
Oscil <COS8192_NUM_CELLS, AUDIO_RATE> aModWidth(COS8192_DATA);
Oscil <COS8192_NUM_CELLS, CONTROL_RATE> kModFreq1(COS8192_DATA);
Oscil <COS8192_NUM_CELLS, CONTROL_RATE> kModFreq2(COS8192_DATA);
Oscil <ENVELOP2048_NUM_CELLS, AUDIO_RATE> aEnvelop(ENVELOP2048_DATA);

// use: Line <type> lineName
Line <long> aGliss;

ReverbTank reverb;

// for fake midi
#include <EventDelay.h>
#include <mozzi_rand.h>
#include <IntMap.h>

#include "PDResonant.h"

unsigned int x_axis = 512; // give a static value for test without midi
unsigned int y_axis = 512;
const IntMap kmapX(0, 1023, 0, 1000); // A
const IntMap kmapY(0, 1023, 0, 3000); //D

PDResonant voice;

// for fake midi
//EventDelay startNote; 
//EventDelay endNote;

// for Line
byte lo_note = 55; // midi note numbers
byte hi_note = 70;

long audio_steps_per_gliss = AUDIO_RATE / 4; // ie. 4 glisses per second
long control_steps_per_gliss = CONTROL_RATE / 4;

// stuff for changing starting positions, probably just confusing really
int counter = 0;
byte gliss_offset = 0;
byte gliss_offset_step = 2;
byte  gliss_offset_max = 36; 

int Selecter = 0; //シリアル通信で音色を変更する

void setup(){
  // synth params
  aCarrier.setFreq(55);
  kModFreq1.setFreq(3.98f);
  kModFreq2.setFreq(3.31757f);
  aModWidth.setFreq(2.52434f);
  aEnvelop.setFreq(9.0f);
  
  randSeed(); // fresh random for fake midi
  pinMode(13, OUTPUT); // for midi feedback
  Serial.begin(9600);
  startMozzi(CONTROL_RATE);
}

/*
void HandleNoteOn(byte channel, byte pitch, byte velocity){
  if (velocity > 0)
  {
    voice.noteOn(channel, pitch, velocity);
    unsigned int attack = kmapX(x_axis);
    unsigned int decay = kmapY(y_axis);
    voice.setPDEnv(attack,decay);
    digitalWrite(13,HIGH);
  }
  else{
    stopNote(channel,  pitch,  velocity);
  }
}

void HandleNoteOff(byte channel, byte pitch, byte velocity){
  stopNote(channel,  pitch,  velocity);
}

void stopNote(byte channel, byte pitch, byte velocity){
  voice.noteOff(channel, pitch, velocity);
  digitalWrite(13,LOW);
}

void fakeMidiRead(){
  static char curr_note;
  static int count = 0;
  if(startNote.ready()){
    //curr_note = 20+rand(40);
    curr_note = 50;
    HandleNoteOn(1,curr_note,127);
    startNote.set(2000);
    startNote.start();
    endNote.set(1000);
    endNote.start();
    
    count ++;
    if(count == 2){
      Selecter = 0; //STOP
      count = 0;
    }
  }
  if(endNote.ready()){
    HandleNoteOff(1,curr_note,0);
  }
}
*/

void updateControl(){

  if(Serial.available() > 0){
    Selecter = Serial.read();
  }

  if(Selecter == 48){
    Selecter = 0; //STOP
  }

  /*
  if(Selecter == 49){
    fakeMidiRead();
    x_axis = 512; //mozziAnalogRead(X);
    y_axis = 512; // mozziAnalogRead(Y);
  
    voice.update();
  }
  */
  
  if(Selecter == 50){
    if (--counter <= 0){
      
      // start at a new note
      gliss_offset += gliss_offset_step;
      if(gliss_offset >= gliss_offset_max){
        gliss_offset=0;
        Selecter = 0; //STOP
      }
      
      // only need to calculate frequencies once each control update
      int start_freq = mtof(lo_note+gliss_offset);
      int end_freq = mtof(hi_note+gliss_offset);
      
      // find the phase increments (step sizes) through the audio table for those freqs
      // they are big ugly numbers which the oscillator understands but you don't really want to know
      long gliss_start = aTriangle.phaseIncFromFreq(start_freq);
      long gliss_end = aTriangle.phaseIncFromFreq(end_freq);
      
      // set the audio rate line to transition between the different step sizes
      aGliss.set(gliss_start, gliss_end, audio_steps_per_gliss);
      
      counter = control_steps_per_gliss;
    }
  }
  
  if(Selecter == 51){
    // synth control
    aModulator.setFreq(277.0f + 0.4313f*kModFreq1.next() + kModFreq2.next());
  }
  
}

int updateAudio(){
  /*
  if(Selecter == 49){
    return voice.next();
  }
  */
  
  // for Line
  if(Selecter == 50){
    aTriangle.setPhaseInc(aGliss.next());
    return aTriangle.next();
  }
  
  // for ReverTank
  if(Selecter == 51){
    int synth = aCarrier.phMod((int)aModulator.next()*(150u+aModWidth.next()));
    synth *= (byte)aEnvelop.next();
    synth >>= 8;
    // here's the reverb
    int arev = reverb.next(synth);
    // add the dry and wet signals
    return synth + (arev>>3);
  }
}

void loop(){
  audioHook(); // required here
}


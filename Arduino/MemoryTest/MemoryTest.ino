#include <MemoryBrute.h>
#include <malloc.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>

/*
extern char _end;
extern "C" char *sbrk(int i);
char *ramstart=(char *)0x20070000;
char *ramend=(char *)0x20088000;
int maxRamSize = 262144;
uint8_t * v;
*/

int memSize;
std::vector<int> arr;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.print("sup");
  /*
  memSize = maxRamSize;
  v = (uint8_t *) malloc(memSize);
  while (v==NULL) {
    memSize -= 1024;
    v = (uint8_t *) malloc(memSize);
    Serial.print("shit1 ");
  }
  while (v!=NULL) {
    memSize += 32;
    v = (uint8_t *) malloc(memSize);
    Serial.print("shit2");
  }
  v = (uint8_t *) malloc(memSize - 32);
  Serial.print("\ngood. Allocated:");
  Serial.println(memSize);
  free(v);
  */
  memSize = checkMemory();

  Serial.print("free memory: ");
  Serial.println(memSize);

  arr.push_back(1);

  // initialize digital pin LED_BUILTIN as an output.
  //pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  arr.push_back(1);
  int s = arr.size();
  /*
  for (int i = 0; i<s; i++) {
    Serial.print("adding");
    arr.push_back(1);
  }
  */
  Serial.print("\narr size: ");
  Serial.println(s);
  /*
  char *heapend=sbrk(0);
  register char * stack_ptr asm ("sp");
  */
  Serial.print("Guess at free mem: ");
  Serial.println(checkMemory());
  delay(1);
   /*
   Serial.println("Program static ram used %d\n",&_end - ramstart);
   

  /*
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
  */
}

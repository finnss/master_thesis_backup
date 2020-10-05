#include "MemoryBrute.h"
#include <malloc.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>

int _maxRamSize = 262144;
uint8_t * _v;
int _memSize;
struct mallinfo _mi;
int _takenMemory;

int checkMemory() {
  _memSize = _maxRamSize;
  _v = (uint8_t *) malloc(_memSize);
  while (_v==NULL) {
    _memSize -= 1024;
    _v = (uint8_t *) malloc(_memSize);
  }
  while (_v!=NULL) {
    free(_v);
    _memSize += 32;
    _v = (uint8_t *) malloc(_memSize);
  }
  free(_v);

  _mi = mallinfo();
  int _takenMemory = _mi.uordblks;

  return _memSize - _takenMemory;
}

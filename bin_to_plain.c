//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

//  Actually, I (Stephanie) butchered this file for my own purposes, possibly
//  to the point that it is almost unrecognisable. The purpose of it now is
//  literally to take whatever binary format the word_2_vec script outputs and
//  turn it back into something pseudo-readable (although it seems downstream
//  processing may still be required).

#include <stdio.h>
#include <string.h>
#include <math.h>
//#include <malloc.h>       /* exclude because I was running this on OS X */
#include <stdlib.h>         /* include because I was running this on OS X */

const long long max_size = 2000;         // max length of strings
const long long max_w = 50;              // max length of vocabulary entries

int main(int argc, char **argv) {
  FILE *f;
  char file_name[max_size], st[100][max_size];
  float len;
  long long words, size, a, b;
  char ch;
  float *M;
  char *vocab;
  if (argc < 2) {
    printf("Usage: ./bin_to_plain <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    return 0;
  }
  strcpy(file_name, argv[1]);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
    return -1;
  }
  for (b = 0; b < words; b++) {
    fscanf(f, "%s%c", &vocab[b * max_w], &ch);
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
  fclose(f);

  // here onwards is my addition (also the rest of the original file
  // (distance.c) is missing from here on)
  FILE *fnb = fopen("google_reps.txt","w");
  for (int i = 0; i < words; i++) {
    for (int p = 0; p<max_w; p++){
        if (vocab[i*max_w+p]!='\0') {
            fprintf(fnb,"%c",vocab[i*max_w+p]);
        }
    }
    fprintf(fnb, "\t");
    for (int j = 0; j < size - 1; j++){
      fprintf(fnb,"%f\t", M[i * size + j]);
    }
    fprintf(fnb, "%f\n", M[i * size + size -1]);
  }
  fclose(fnb);

  return 1;
}

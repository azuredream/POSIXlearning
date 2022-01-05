/*
* Print tools
* Created on 1.4.2022
* ZZX
*/

#include <stdio.h>

// Print messages based on different running level
// v0: error               (defaut)
// v1: error, warning
// v2: error, warning, msg


void lprint_err(char* str, int lv) {
    if (lv >= 0)
    {   
        printf("Error: %s", str);
        printf("\n");
    }
} 

void lprint_war(char* str, int lv) {
    if (lv >= 1)
    {   
        printf("Warning: %s", str);
        printf("\n");
    }
} 

void lprint_msg(char* str, int lv) {
    if (lv >= 2)
    {   
        printf("Message: %s", str);
        printf("\n");
    }
} 


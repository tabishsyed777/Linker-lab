#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
extern long ledger_quote(long, long);
int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: ledgercalc cents quantity\n"); return 2; }
    char *a, *b;
    errno = 0;
    long cents = strtol(argv[1], &a, 10), quantity = strtol(argv[2], &b, 10);
    if (errno || !argv[1][0] || !argv[2][0] || *a || *b || cents < -1000000 || cents > 1000000 || quantity < 0 || quantity > 10000) return 2;
    printf("%ld\n", ledger_quote(cents, quantity));
    return 0;
}

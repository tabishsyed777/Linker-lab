extern long money_subtotal(long, long);
long ledger_quote(long cents, long quantity) { return money_subtotal(cents, quantity) + 7; }

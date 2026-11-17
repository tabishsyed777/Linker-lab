cmake_minimum_required(VERSION 3.20)
project(ledgercalc C)
add_library(money SHARED money.c)
add_library(ledger SHARED ledger.c)
add_executable(ledgercalc main.c)
# Incident: ledger's dependency is missing, and install/runtime paths are incomplete.
target_link_libraries(ledgercalc PRIVATE ledger)
install(TARGETS ledgercalc RUNTIME DESTINATION bin)

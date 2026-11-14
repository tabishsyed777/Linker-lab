# Repair a relocatable native CLI installation

The C sources in `/app/project` are correct, but the CMake build/install configuration is broken. Repair only `/app/project/CMakeLists.txt`.

Required outcome:

- A clean CMake configure/build/install succeeds with any supplied install prefix.
- The installed tree contains `bin/ledgercalc`, `lib/libledger.so`, and `lib/libmoney.so`.
- These are real shared libraries: ledgercalc dynamically depends on libledger.so and libledger.so dynamically depends on libmoney.so. Do not replace them with static libraries or a script.
- After the installed tree is copied to a different path (possibly containing spaces), it still runs from an unrelated working directory with LD_LIBRARY_PATH and LD_PRELOAD absent. No absolute build/source directory or loader environment overrides may be needed.
- `ledgercalc CENTS QUANTITY` prints exactly `CENTS * QUANTITY + 7` followed by a newline. The documented integer range is -1,000,000..1,000,000 cents and 0..10,000 quantity. Invalid arguments exit 2.

The verifier rebuilds from your CMakeLists.txt and pristine copies of the provided C sources. Other edits and prebuilt artifacts are not submitted. Normal build tools, compiler, cmake, readelf, and nm are available. Build and inspect locally as needed.

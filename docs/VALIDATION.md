# LinkerLab validation

Tests-first development began with failing imports/CLI execution before the runner existed. Three verifier/runner unit tests and a real Docker integration test were then made green. A further tests-first unit check now rejects Harbor results with an unexpected reward or an exception, even when its CLI exited successfully.

The current suite has four unit tests and one container integration test. The integration test accepts the reference configuration, rejects the unchanged starter, rejects the static-library shortcut, checks that evidence was generated, and checks refusal to overwrite prior output.

The accepted reference passes 17 outcome checks: clean configure/build/install, required installed files, two dynamic-library dependencies, six computations after relocation into a path with spaces with loader overrides absent, and three invalid-argument behaviors. Expected arithmetic is evaluated independently in Python. The unchanged starter fails clean linking; the static shortcut fails the required shared-library layout.

Actual Harbor 0.26.0 local-Docker trials with separate verification produced oracle reward 1 and NOP reward 0, both with reward_valid=true and no exception. Schema version 1.4 was validated with that installed Harbor version. Initial concurrent trials encountered disk exhaustion; those infrastructure failures were excluded, free space was restored, and fresh sequential trials produced the results above. A workspace-only wrapper relocated Harbor's cache constants because the managed environment's home is read-only; task/verifier execution was not modified.

No model/terminal agent was evaluated. These public synthetic controls establish implemented behavior and task solvability, not meaningful difficulty, secrecy, official benchmark acceptance, or a complete hostile-code sandbox. The container images use a moving base tag and apt packages; recorded image IDs identify the measured local image but this is not a fully pinned build.

# Development plan: reliable detailed analysis in Docker

Status: implemented and verified in the supported Docker runtime. The operator
approved the analysis-only Docker system-path exception. Both Compose preflights
and controlled real reports passed. See the execution record below.

## Intended outcome

Both `--forecast-window 5` and `--forecast-window 10` can run inside the analysis
container, read the required local feature references, use web search, and save
reports. A blocked execution sandbox must stop the workflow with an actionable
error before existing reports are deleted or analysis requests are sent.

Detailed report generation must not initialize MCP connections inherited from
the developer's personal Codex configuration. A Codex process that exits zero
after an unrecovered infrastructure failure must not produce a report labelled
as successfully generated.

## Evidence and remaining uncertainty

The execution path is:

`run_detailed_analysis.py -> detailedAnalysis/main.py -> llm_runner/codex_runner.py:run_codex()`

- The synchronous runner explicitly requests `--sandbox read-only`, but loads
  the user's Codex configuration. The asynchronous chat runner already uses
  `--ignore-user-config` and explicitly configures its MCP endpoint.
- The analysis Dockerfile installs Codex but omits `bubblewrap` and `ripgrep`.
  The supplied log shows Codex's bundled bubblewrap failing to create a namespace.
- Inspection of the running assistant container, which uses the same image and
  named Codex volume, confirmed that `bwrap` is absent and seccomp filtering is
  active. Namespace failure is established by the supplied analysis log; whether
  seccomp, capabilities, or host policy causes the denial remains to be isolated.
- The shared volume's `/root/.codex/config.toml` contains
  `http://localhost:8003/mcp`. The current host configuration contains
  `http://127.0.0.1:8004/mcp`. The entrypoint copies the entire host Codex directory
  only when the volume has no `config.toml`, preserving outdated settings.
- Compose publishes REST on host port 8003 and MCP on host port 8004 by default.
  The MCP address within the Compose network is `http://agentic-mcp:8000/mcp`.
- The batch runner clears the output directory before retrieving data or starting
  Codex. The synchronous runner checks only the overall process exit status.

## Scope and constraints

Preserve the current technical-data contract, forecast selection, model choice,
web-search behavior, and local feature-reference workflow. Do not add generated
feature definitions to the prompt as a workaround for broken filesystem access.

Keep `read-only` sandboxing as the default. Do not automatically retry with
`danger-full-access`, a privileged container, or broadly relaxed host settings.
Any runtime exception must be justified by a reproducible sandbox failure and
limited to the analysis service.

The shared synchronous runner also serves entry and hold strategies. Test those
callers when changing it. The asynchronous chat runner's MCP configuration must
continue to work independently.

## Phase 1: isolate detailed analysis from personal Codex settings

Files: `llm_runner/codex_runner.py`, `tests/test_codex_runner.py`.

1. Add `--ignore-user-config` to synchronous `run_codex()`. Codex authentication
   remains in `CODEX_HOME`; this flag skips user configuration, not authentication.
2. Set `approval_policy="never"` explicitly for the unattended process, so a
   blocked tool fails predictably instead of relying on a personal approval policy.
3. Continue passing the existing model, reasoning effort, search flag, working
   directory, and sandbox policy explicitly.
4. Verify whether enabled plugins or project configuration can still initialize
   unwanted MCP connections in the pinned CLI. Disable plugins for this runner
   if needed; check project configuration separately rather than assuming that
   ignoring user configuration suppresses every source.

Acceptance: a run with a deliberately stale user MCP entry does not contact it,
works with existing authentication, and still supports `--search`. Report
generation works with the report MCP service stopped.

## Phase 2: install sandbox prerequisites and prove runtime compatibility

Files: `Dockerfile`, `docker-compose.yml` only if a runtime change is necessary,
plus a small reusable diagnostic/preflight module or script.

1. Install distribution `bubblewrap` and `ripgrep` alongside `ca-certificates`.
   Verify `bwrap` and `rg` are on PATH in the rebuilt image.
2. Use the pinned CLI's Linux sandbox diagnostic command, after checking its
   supported syntax inside Linux, to execute a fixed read-only smoke command.
   The smoke command must read `/app/instructions/README.md`, the feature guide,
   and the feature index through the actual Codex sandbox. A plain Python read
   outside the sandbox is insufficient.
3. Reproduce under the normal Compose settings first. If namespace creation is
   still denied, inspect user-namespace support, seccomp, capabilities, and host
   AppArmor policy. Diagnose the execution host's Linux runtime; macOS sysctl
   changes cannot configure Docker Desktop's Linux namespace policy.
4. Implement the smallest demonstrated runtime fix. Prefer a narrowly scoped
   seccomp/profile adjustment if that is the blocker. Do not assume that package
   installation alone resolves namespace permissions, and do not prescribe
   `SYS_ADMIN` or an unconfined profile without showing why it is necessary.
5. Record the tested Docker/runtime versions and the actual remedy in README.
   If sandbox support cannot be provided, return a clear unsupported-runtime
   error; keep any alternative execution architecture as separate work.

Acceptance: the sandbox smoke command succeeds in the same service, user,
working directory, and configuration used for analysis. Startup has no missing
bubblewrap warning and file-read commands have no namespace errors.

## Phase 3: preflight before destructive batch preparation

Files: `run_detailed_analysis.py`, `detailedAnalysis/main.py`, diagnostic/preflight
module, `tests/test_run_detailed_analysis.py`, `tests/test_detailed_analysis_main.py`.

1. After loading environment settings and resolving the forecast window, check
   the Codex executable, selected instructions, and the sandbox smoke command.
2. Run the batch-level sandbox preflight once before `prepare_output_dir()` and
   before fetching recommendations, stocks, or technical data. Bound its runtime.
3. Keep per-ticker checks for relevant catalog references after obtaining the
   validated payload. Verify that known supplied features have readable matching
   cards; retain the documented limitations for genuinely uncatalogued features.
4. Ensure direct calls to the individual analysis function receive the same
   guarantees, without repeating the expensive sandbox preflight for every
   ticker in a batch. Use an explicit internal handoff of a successful preflight.
5. Return a nonzero status on preflight failure. Include the failed check and
   relevant sanitized stderr, rather than only `Codex execution failed`.

Acceptance: simulated namespace denial prevents HTTP requests, Codex generation,
and output-directory cleanup. Existing reports remain byte-for-byte intact.

## Phase 4: distinguish process completion from usable report completion

Files: `llm_runner/codex_runner.py`, `app/errors.py` if needed,
`detailedAnalysis/main.py`, runner and pipeline tests.

1. Add a configurable generation timeout, separate from the technical API HTTP
   timeout. Terminate and reap timed-out processes and remove temporary output.
2. Run Codex with structured events (`--json`) and capture bounded diagnostic
   output. Verify the event schema emitted by the pinned CLI before implementing
   event parsing; do not invent event names or depend on unstable log wording.
3. Treat process failure, timeout, missing/empty final output, and an unrecovered
   sandbox/infrastructure failure as generation failure, even if the final
   process exit code is zero. Allow a transient failed tool call that is later
   demonstrably recovered; do not reject every nonzero shell exit indiscriminately.
4. If events do not provide a stable, machine-checkable infrastructure signal,
   document that limitation and use narrowly tested diagnostic matching plus
   the preflight. Do not claim that these checks prove the model read every card
   or that the analysis is financially correct.
5. Generate into a temporary file in the report directory. Publish with atomic
   file replacement only after validation, and remove temporary files on failure.
   Keep "Analysis saved" after the validated publication step.
6. Keep raw prompts, technical payloads, credentials, and full environment values
   out of user-facing error logs. Retain only bounded, sanitized diagnostics.

Acceptance: a fake Codex executable that exits zero, reports namespace failure,
and writes a fallback answer is rejected. Missing and empty output are rejected;
timeouts clean up; a healthy run publishes a nonempty report. A recovered tool
failure does not cause a false rejection.

## Phase 5: make container authentication bootstrapping predictable

Files: `docker-entrypoint.sh`, `README.md`, `.env.example` as needed.

1. Replace copying the entire host Codex home on first startup with an explicit
   authentication-only bootstrap compatible with the pinned CLI. Verify the
   supported credential-storage mode and preserve the API-key authentication path.
2. Do not copy personal MCP settings, plugins, or unrelated configuration into
   a new container volume. Do not print credential contents.
3. Existing volumes must remain usable without deletion or reauthentication.
   Phase 1 makes stale configuration harmless for generation; document a targeted
   optional migration for the copied configuration instead of deleting the volume.
4. Clarify REST versus MCP host ports and the Compose MCP service address.
   Describe the namespace preflight, supported runtime remedy, and diagnostics.

Acceptance: fresh bootstrapping imports only necessary credentials; existing
volumes still authenticate; unrelated Codex state is untouched. The chat runner
continues to use its explicitly configured MCP URL.

## Verification and rollout

1. Extend runner tests with a fake executable and real temporary files, rather
   than checking command arguments alone. Cover stale MCP configuration,
   infrastructure failure with exit zero, output validation, timeout, and cleanup.
2. Extend batch/pipeline tests for preflight ordering and preservation of reports
   when preflight fails. Exercise both horizons and the documented unknown-feature
   limitation. Run entry/hold strategy regressions because they share the runner.
3. Resolve the existing test expectation discrepancy deliberately: the synchronous
   runner selects `gpt-5.6-sol`, while its command test expects `gpt-6.1-sol`.
   Keep the current runtime model for this issue and align the expectation unless
   a separate model change is explicitly requested.
4. Run the focused unittest suites, followed by the repository suite once focused
   checks pass. Mock external data services; unit tests must not spend model tokens.
5. Rebuild the analysis image and run the sandbox preflight inside Compose.
   Reuse a volume containing the stale MCP URL to prove configuration isolation.
6. Run one controlled real report for each horizon with valid data and available
   authentication. Record model-generated reference reads and successful report
   publication; inspect the reports for infrastructure fallback text. This is
   an end-to-end check, not proof of every financial interpretation.
7. Exercise a deliberately blocked runtime using disposable output fixtures.
   Confirm nonzero exit, actionable diagnostics, and preservation of fixtures.

Suggested implementation order: Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5.
The runtime smoke test is a release gate: configuration isolation alone does not
resolve inaccessible local references.

The current early clearing of output after a successful preflight is a separate
remaining risk if generation later fails. A future batch-staging change can
preserve prior reports across every generation failure; do not describe
per-report atomic writes as an atomic replacement of an entire rolling window.

## Completion criteria

- Both detailed-analysis forecast windows succeed in the supported container.
- Codex can read the required local references through its sandbox.
- Stale personal MCP configuration cannot affect report generation.
- Runtime startup failures occur before output cleanup and model requests.
- Unrecovered sandbox failures cannot be saved as successful new reports.
- Existing authentication and shared-runner callers pass regression checks.
- README documents the verified runtime setup and targeted migration steps.

## Reference

[Official OpenAI sandbox prerequisites](https://learn.chatgpt.com/docs/sandboxing#prerequisites)

The CLI help for the installed `0.146.0` version confirms that
`--ignore-user-config` skips `$CODEX_HOME/config.toml` while authentication still
uses `CODEX_HOME`, and that `--json` emits JSONL events. Verify Linux diagnostic
syntax and event details in the implementation environment.


## Execution record — 2026-10-10

Implemented phases 1, 3, 4, and 5: isolated synchronous configuration, explicit
never approvals, bounded generation timeout/capture, validated JSONL and final
output, atomic per-report publication, batch/direct-call sandbox preflight,
matching feature-card checks, and authentication-only bootstrapping. Model remains
`gpt-5.6-sol`; the asynchronous chat MCP configuration is unchanged.

Phase 2 installs bubblewrap/ripgrep and adds an analysis-only scoped seccomp
profile after reproducing namespace denial. Linux diagnostic syntax was verified
against Codex 0.146.0. Event fields were checked using the official pinned SDK.
A second reproduced restriction (Docker masked proc mounts) prevents distribution
bubblewrap mounting proc even when seccomp is unconfined. A disposable smoke test
passed with system-path masks removed. Automatic approval review rejected applying
`systempaths=unconfined` persistently because it weakens container isolation.
Default Compose does not enable that exception. The optional
`docker-compose.sandbox-runtime.yml` is prepared for operator approval; README
records tested runtime versions, reproduction, risks and the pending gate.

Verification: focused regressions passed, followed by the repository suite
(136 tests at the final full-suite run). Fake executable tests cover exit-zero
infrastructure failure, missing/empty final output, timeout cleanup, healthy
publication and successful recovery of the same failed command. Pipeline tests
cover both horizons and unknown-feature limitations. Authentication tests cover
fresh and existing volumes without exposing credentials. The blocked-runtime
fixture check preserves prior reports and prevents requests and generation.

Pending release work: obtain operator approval or supply a compatible runtime;
pass both Compose sandbox preflights; prove stale MCP isolation with the pinned
live CLI; generate one controlled real report per horizon and inspect recorded
reference reads and output. Do not mark completion criteria satisfied until these
runtime checks pass.


### Approved runtime verification

The operator explicitly approved enabling the override and verifying both
forecast windows. Default Compose now includes `systempaths=unconfined` only for
`agentic-stock-analysis`; the scoped seccomp profile and read-only Codex sandbox
remain in place. Both 5- and 10-session Compose preflights passed with the existing
Codex volume. The optional override is redundant with the approved default.
Controlled AALI reports for both horizons were generated into the separate
`detailedAnalysisResults/verification/` directory. Both exited zero, emitted
completed turns, and published nonempty output atomically: 34,226 bytes for 5dd
and 36,869 bytes for 10dd. Recorded successful commands read the guide/index and
feature references; web-search event counts were 11 and 8 respectively. Both
runs used the existing authenticated volume containing the stale MCP entry;
neither emitted MCP tool calls or namespace-error diagnostics. Published reports
were inspected for infrastructure fallback text and none was found. Sanitized
event evidence is stored beside each report. Existing reports were preserved.
The repository regression suite remains at 136 passing tests; the approval
follow-up changed Compose and documentation only.

The earlier pending-release statements above record the pre-approval state.
Runtime approval, both smoke tests, and both controlled real-report checks have
now completed. Full multi-ticker production batches were not run as verification;
normal batch commands are ready for the operator. Financial correctness and
reading every reference card remain outside what these execution checks prove.

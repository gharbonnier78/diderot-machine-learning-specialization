# Diderot ML Lab — Change Impact & Regression Evidence

This lab is an executable companion to the Test Authority methodological work on change-impact analysis, regression selection, coverage, detection power and accountable evidence.

It is deliberately **more than a toy**, but remains lightweight enough for a laptop or Google Colab.

## Scientific question

Regression testing is often operationalized as test-suite selection. This lab starts one step earlier:

```text
change
  -> plausible propagation
    -> failure mechanism
      -> consequence
        -> evidence need
          -> regression selection
            -> coverage
              -> detection power
```

The central experimental separation is:

```text
G_true != G_observed
```

- `G_true` is the simulator's hidden ground-truth propagation graph.
- `G_observed` is the incomplete/noisy engineering view available to selectors.
- selectors are scored only after they have made their decision.

This prevents the trivial experiment in which the selector is handed the truth it is supposed to discover.

## Synthetic system

`scenarios/identity_platform.yaml` defines a synthetic distributed identity platform with UI/API, enrollment, identity, authentication, biometric and risk services, messaging, databases/cache, configuration/security, device/supplier chain, ML/data elements and observability.

It is **not** a representation of an IN Groupe production architecture.

The graph includes propagation through calls/control, schemas/messages, shared state, timing, resource contention, configuration, security, supplier/device/sensor chains, data and ML dependencies. Some true edges are explicitly hidden from the engineering view; additional edges may be randomly omitted or spurious edges inserted.

## Initial changes

| Change | Main mechanism |
|---|---|
| `CHG_CACHE_TTL` | shared state / stale authorization |
| `CHG_IDENTITY_EVENT_V2` | schema and asynchronous messaging |
| `CHG_EVENTBUS_POOL` | timing/resource propagation |
| `CHG_SUPPLIER_SDK` | supplier/device compatibility |

Propagation is stochastic and seed-controlled; these are not hard-coded expected answers.

## Regression strategies

| Strategy | Description |
|---|---|
| R0 | complete existing regression suite |
| R1 | historical test/change relevance |
| R2 | code/control graph reachability |
| R3 | multi-layer observed system graph |
| R4 | R3 plus consequence/criticality-aware selection |
| R5 | R4 plus learned candidate-impact probabilities from past labelled changes |

R5 currently uses a deliberately simple logistic-regression baseline. It is an **AI-assisted research baseline**, not a production AI agent and not a claim of superiority. The current hidden change outcome is excluded from R5 training; historical labels emulate previously investigated incidents.

## Test, coverage and explicit fault-injection model

Each test declares system elements it exercises, relative execution cost, failure modes it can detect, modeled probability of detection for each mode and historical relevance by change category.

The lab now also contains an explicit **fault-injection plane** independent of change propagation. `faults.py` can build a catalogue from declared node failure modes or run a manually controlled set of injected faults. For each fault the campaign records:

- whether the affected node was covered by the selected regression set;
- the modeled probability that the selected oracles detect that failure mode;
- a seed-controlled realized detection outcome.

This makes it possible to exhibit the important counterexample directly: a node may be covered while the selected oracle has zero detection probability for the injected failure mode.

```text
Coverage != Detection != Decision Evidence
```

The current injection layer is intentionally simple: it perturbs declared failure modes rather than source ASTs or deployed services. It therefore acts as a controlled experimental analogue of mutation/fault injection, not as a replacement for a real mutation-testing engine.

## Metrics

The first implementation reports impact recall, critical-impact recall, impacted-node coverage, critical-node coverage, mean POD, critical mean/minimum POD, critical zero-detection miss rate, realized stochastic detection rate, execution cost and tests executed.

Fault campaigns additionally report node coverage, mean modeled POD, realized detection score and critical mean POD.

These metrics remain separate. No single scalar is treated as sufficient release evidence.

## Run locally

From repository root:

```bash
python -m pip install -e .
jupyter notebook labs/change-impact-regression/00_change_impact_regression_lab.ipynb
```

The automated tests are included in the normal repository test suite:

```bash
make test
```

## Colab

Open `labs/change-impact-regression/00_change_impact_regression_lab.ipynb` in Google Colab. Its bootstrap first tries `main` and, while the pull request is under review, falls back to `lab/change-impact-regression-simulator`.

## Core code

```text
src/diderot_mls/change_impact/
  models.py          typed scenario, change and test contracts
  scenario.py        YAML loader and validation
  simulator.py       hidden graph, observed graph and stochastic propagation
  selectors.py       R0-R5
  metrics.py         coverage/detection/evidence metrics
  faults.py          controlled fault catalogue and injection campaigns
  experiment.py      reproducible comparison and Monte Carlo sweep
  visualization.py   architecture and post-hoc impact overlays
```

## Reproducibility

Randomness is controlled independently for observed-graph degradation, true propagation and realized detection. This allows one uncertainty source to vary while the others are held fixed.

The current automated suite contains eight dedicated lab invariants: six for scenario/graph/selector behavior and two specifically checking the fault-injection plane, including the case `covered == True` with `POD == 0` because the oracle is inappropriate.

## What this lab does not prove

The simulator does not establish production propagation probabilities, real defect frequencies, real test POD, superiority of selective regression, superiority of AI, or a release threshold. Those require studies on real change histories, independently adjudicated regressions, representative environments and preregistered endpoints.

## Planned extensions

1. explicit environment representativity and observability parameters;
2. richer mutation operators, correlated/multi-fault injections and eventually adapters to real mutation-test outputs;
3. richer temporal/resource simulation with SimPy;
4. evidence-actionability layer and reversible triage/grouping;
5. multiple independently generated system topologies;
6. cross-system train/test for R5 to reduce same-topology optimism;
7. Gymnasium-compatible interface for sequential evidence acquisition;
8. Bayesian experimental design / active test recommendation;
9. calibrated confidence intervals and hypothesis tests over strategy deltas;
10. import of anonymized real change histories when governance permits.

The design intentionally keeps RL and more sophisticated ML out of v0 so the deterministic engineering baselines remain inspectable and falsifiable.

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx


def _layout(graph):
    return nx.spring_layout(nx.DiGraph(graph), seed=42, k=0.9)


def plot_system_graph(scenario, graph, *, title=None, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(14, 9))
    pos = _layout(graph)
    simple = nx.DiGraph(graph)
    kinds = sorted({scenario.nodes[n].kind for n in simple.nodes})
    for kind in kinds:
        nodes = [n for n in simple.nodes if scenario.nodes[n].kind == kind]
        nx.draw_networkx_nodes(
            simple, pos, nodelist=nodes,
            node_size=[500 + 120 * scenario.nodes[n].criticality for n in nodes],
            label=kind, ax=ax, alpha=0.85)
    nx.draw_networkx_edges(simple, pos, ax=ax, arrows=True,
                           alpha=0.35, width=1.2)
    nx.draw_networkx_labels(simple, pos, ax=ax, font_size=8)
    ax.set_title(title or scenario.name)
    ax.axis("off")
    ax.legend(loc="best", fontsize=8)
    return ax


def plot_selection_overlay(scenario, graph, outcome, selection, *,
                           title=None, ax=None):
    """Post-hoc truth/prediction comparison; never used by a selector."""
    if ax is None:
        _, ax = plt.subplots(figsize=(14, 9))
    pos = _layout(graph)
    simple = nx.DiGraph(graph)
    true_impacted = outcome.impacted_nodes
    predicted = selection.predicted_impacts
    covered = set()
    for test_id in selection.selected_tests:
        covered.update(scenario.tests[test_id].covers)
    categories = {
        "true+predicted": true_impacted & predicted,
        "true missed by impact model": true_impacted - predicted,
        "predicted only": predicted - true_impacted,
        "other": set(simple.nodes) - (true_impacted | predicted),
    }
    for label, nodes in categories.items():
        if not nodes:
            continue
        ordered = sorted(nodes)
        nx.draw_networkx_nodes(
            simple, pos, nodelist=ordered,
            node_size=[520 + 120 * scenario.nodes[n].criticality +
                       (120 if n in covered else 0) for n in ordered],
            label=label, ax=ax, alpha=0.85)
    nx.draw_networkx_edges(simple, pos, ax=ax, arrows=True,
                           alpha=0.25, width=1.0)
    nx.draw_networkx_labels(simple, pos, ax=ax, font_size=8)
    ax.set_title(title or f"{selection.strategy}: realized vs predicted impact")
    ax.axis("off")
    ax.legend(loc="best", fontsize=8)
    return ax

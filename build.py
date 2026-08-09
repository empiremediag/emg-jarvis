#!/usr/bin/env python3
"""Build viewer/graph-data.js from agents.json.

Python 3 standard library only. Reads the flat agent list in agents.json and
writes a 3d-force-graph compatible `GRAPH = {nodes, links}` object that the
viewer loads directly as a <script> tag.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_PATH = os.path.join(BASE_DIR, "agents.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "viewer", "graph-data.js")

GROUP_COLORS = {
    "SUPER_AGENTS": "#C9A84C",
    "VOICE_AI": "#00E5FF",
    "CONVERSATION_AI": "#00C896",
}


def load_agents():
    with open(AGENTS_PATH, "r") as f:
        return json.load(f)


def build_graph(agents):
    nodes = []
    for i, agent in enumerate(agents):
        if agent.get("id") != i:
            raise ValueError(
                f"agents.json entry {i} has id={agent.get('id')!r}, "
                "expected id to equal array index"
            )
        nodes.append({
            "id": agent["id"],
            "label": agent["label"],
            "group": agent["group"],
            "type": agent["type"],
            "status": agent["status"],
            "tools": agent["tools"],
            "description": agent["description"],
            "linkedAgents": agent.get("linkedAgents", []),
            "color": GROUP_COLORS.get(agent["group"], "#888888"),
        })

    seen = set()
    links = []
    for agent in agents:
        source = agent["id"]
        for target in agent.get("linkedAgents", []):
            if target == source:
                continue
            key = tuple(sorted((source, target)))
            if key in seen:
                continue
            seen.add(key)
            links.append({"source": source, "target": target})

    return {"nodes": nodes, "links": links}


def main():
    agents = load_agents()
    graph = build_graph(agents)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("const GRAPH = ")
        json.dump(graph, f, indent=2)
        f.write(";\n")

    print(
        f"build.py: wrote {len(graph['nodes'])} nodes and "
        f"{len(graph['links'])} links -> {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()

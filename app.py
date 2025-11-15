from flask import Flask, jsonify, request
from graph_data import graph
from dijkstra import dijkstra_with_constraints
from coloring import build_adjacency_list, graph_coloring

app = Flask(__name__)

@app.get("/graph")
def get_graph():
    return jsonify(graph)

@app.get("/dijkstra")
def api_dijkstra():
    source = request.args.get("src")

    if source not in graph:
        return jsonify({"error": "Noeud source introuvable"}), 400

    distances = dijkstra_with_constraints(source)
    return jsonify(distances)


@app.get("/coloring")
def api_coloring():
    simple = build_adjacency_list(graph)
    colors = graph_coloring(simple)
    return jsonify(colors)


if __name__ == "__main__":
    app.run(debug=True)

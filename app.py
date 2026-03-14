from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from dijkstra import dijkstra

app = Flask(__name__)

graph = {
'A': {'B':4,'C':3},
'B': {'A':4,'D':5,'E':2},
'C': {'A':3,'F':7},
'D': {'B':5,'G':6},
'E': {'B':2,'H':4},
'F': {'C':7,'I':3},
'G': {'D':6,'J':5},
'H': {'E':4,'K':6},
'I': {'F':3,'L':4},
'J': {'G':5,'M':2},
'K': {'H':6,'N':3},
'L': {'I':4,'O':7},
'M': {'J':2,'P':6},
'N': {'K':3,'Q':5},
'O': {'L':7,'R':4},
'P': {'M':6,'S':3},
'Q': {'N':5,'T':6},
'R': {'O':4,'U':2},
'S': {'P':3,'V':5},
'T': {'Q':6,'W':4},
'U': {'R':2,'X':3},
'V': {'S':5,'Y':6},
'W': {'T':4,'Z':5},
'X': {'U':3},
'Y': {'V':6},
'Z': {'W':5}
}

def draw_graph(graph, path):

    G = nx.Graph()

    for node in graph:
        for neighbour, weight in graph[node].items():
            G.add_edge(node, neighbour, weight=weight)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(7,5))

    nx.draw(
        G, pos,
        with_labels=True,
        node_size=1800,
        node_color="#a8d8ff",
        font_size=10,
        font_weight="bold",
        edge_color="gray"
    )

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=9)

    # highlight shortest path
    path_edges = list(zip(path, path[1:]))

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=path_edges,
        edge_color="red",
        width=3
    )

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()

    plt.close()

    return graph_url


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/route', methods=['POST'])
def route():

    start = request.form['start'].upper()
    end = request.form['end'].upper()

    if start not in graph or end not in graph:
        return "Invalid Node! Use A-Z"

    distance, path = dijkstra(graph, start, end)

    graph_url = draw_graph(graph, path)

    return render_template("index.html", distance=distance, graph_url=graph_url)


if __name__ == "__main__":
    app.run(debug=True)
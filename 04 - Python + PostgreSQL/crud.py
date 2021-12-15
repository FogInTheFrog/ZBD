from sqlalchemy.orm import Session


def create_graph(db: Session):
    edges_dict = dict()
    edges = db.execute("SELECT * FROM undirected_edges").fetchall()

    for edge in edges:
        (a, b) = edge
        edges_dict[a].append(b)
        edges_dict[b].append(a)

    return edges_dict


def get_shortest_path(db: Session, start_id: int, end_id: int, graph=None):
    visited = set()
    depths = dict()
    paths = dict()
    queue = []
    queue_it = 0

    if graph:
        my_graph = graph
    else:
        my_graph = create_graph(db)

    queue.append(start_id)
    visited.add(start_id)
    depths[start_id] = 0

    while queue_it < len(queue):
        x = queue[queue_it]
        vertex_list = my_graph[x]
        queue_it += 1

        for v in vertex_list:
            if v not in visited:
                visited.add(v)
                queue.append(v)
                depths[v] = depths[x] + 1
                paths[v] = x

    my_node = end_id
    path = []
    while my_node != start_id:
        path.append(my_node)
        my_node = paths.get(my_node)

    path.append(start_id)

    return path

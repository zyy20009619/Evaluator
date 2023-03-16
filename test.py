def invocation(method_id, explored, invoke_methods, local_contain):
    if method_id not in invoke_methods:
        return explored

    next_invocations = list()
    for called_id in invoke_methods[method_id]:
        if called_id not in explored and method_id != called_id and called_id in local_contain:
            next_invocations.append(called_id)
    if len(next_invocations) > 0:
        explored[method_id] = next_invocations
        for next_invocation in next_invocations:
            invocation(next_invocation, explored, invoke_methods, local_contain)
    return explored


def get_called_values(arrays):
    res = list()
    for item1 in arrays:
        res.extend(item1)
    return res


if __name__ == '__main__':
    invoke_methods = {'A': ['B', 'F'], 'B': ['C', 'E'], 'C': ['D', 'G'], 'F': ['E']}
    local_contain = ['A', 'B', 'C', 'E', 'F', 'G']

    res = list()
    for called_id in invoke_methods['A']:
        res.extend(get_called_values(invocation(called_id, dict(), invoke_methods, local_contain).values()))
    # res = [item for item in res]
    print(set(res))

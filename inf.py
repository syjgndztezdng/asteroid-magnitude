n, m = map(int, input().split())

adj = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

visited = [False] * (n + 1)
components = []

for i in range(1, n + 1):
    if not visited[i]:
        comp = []
        stack = [i]
        visited[i] = True
        while stack:
            curr = stack.pop()
            comp.append(curr)
            for neighbor in adj[curr]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
        components.append(comp)

print(len(components))
for comp in components:
    print(len(comp))
    print(*comp)

n, m = map(int, input().split())

adj = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

color = [0] * (n + 1)
possible = True

for i in range(1, n + 1):
    if color[i] == 0:
        color[i] = 1
        stack = [i]
        while stack:
            curr = stack.pop()
            for neighbor in adj[curr]:
                if color[neighbor] == 0:
                    color[neighbor] = 3 - color[curr]
                    stack.append(neighbor)
                elif color[neighbor] == color[curr]:
                    possible = False
                    break
            if not possible:
                break
    if not possible:
        break

if possible:
    print("YES")
    first_table = [i for i in range(1, n + 1) if color[i] == 1]
    print(*first_table)
else:
    print("NO")

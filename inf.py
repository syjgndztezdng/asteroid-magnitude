n = int(input())
adj = [list(map(int, input().split())) for _ in range(n)]

edges = 0
for i in range(n):
    for j in range(i + 1, n):
        if adj[i][j] == 1:
            edges += 1

if edges != n - 1:
    print("NO")
else:
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 0

    while stack:
        curr = stack.pop()
        count += 1
        for neighbor in range(n):
            if adj[curr][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)

    if count == n:
        print("YES")
    else:
        print("NO")

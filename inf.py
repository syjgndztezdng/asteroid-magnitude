n, s = map(int, input().split())
adj = [list(map(int, input().split())) for _ in range(n)]

start = s - 1
visited = [False] * n
stack = [start]
visited[start] = True
count = 0

while stack:
    curr = stack.pop()
    count += 1
    for neighbor in range(n):
        if adj[curr][neighbor] == 1 and not visited[neighbor]:
            visited[neighbor] = True
            stack.append(neighbor)

print(count)

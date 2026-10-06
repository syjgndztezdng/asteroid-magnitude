m, n = map(int, input().split())
grid = [input().strip() for _ in range(m)]

visited = [[False] * n for _ in range(m)]
components = 0

for i in range(m):
    for j in range(n):
        if grid[i][j] == '#' and not visited[i][j]:
            components += 1
            visited[i][j] = True
            stack = [(i, j)]
            
            while stack:
                r, c = stack.pop()
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n:
                        if grid[nr][nc] == '#' and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))

print(components)

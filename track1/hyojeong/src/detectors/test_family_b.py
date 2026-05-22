from typing import List, Dict, Tuple

# =====================================================================
# Step 2 & 4: Typed Contract & Actual Implementation (Family B)
# =====================================================================

def check_line_of_sight(grid: List[List[int]], p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
    """
    Bresenham's Line Algorithm을 단순화하여 두 점(p1, p2) 사이에 
    벽(1)이 있는지 검사합니다. (0은 빈 공간, 1은 벽)
    """
    x0, y0 = p1
    x1, y1 = p2
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x_sign = 1 if x0 < x1 else -1
    y_sign = 1 if y0 < y1 else -1

    err = dx - dy
    while True:
        if grid[y0][x0] == 1: # 벽에 부딪힘
            return False
        if x0 == x1 and y0 == y1: # 장애물 없이 도착
            return True
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += x_sign
        if e2 < dx:
            err += dx
            y0 += y_sign

def detect_l42_interactional_visibility(grid: List[List[int]], positions: List[Tuple[int, int]]) -> bool:
    """
    L42 Interactional Visibility Detector
    공간 안의 사람들(positions) 중 서로 시야가 닿는(벽이 없는) 쌍이 있는지 확인합니다.
    """
    n = len(positions)
    if n < 2:
        return False
        
    for i in range(n):
        for j in range(i + 1, n):
            # 두 사람 사이에 시야가 뚫려있으면 True
            if check_line_of_sight(grid, positions[i], positions[j]):
                return True
    return False

def detect_l17_prospect(grid: List[List[int]], point: Tuple[int, int], min_prospect_dist: int = 4) -> bool:
    """
    L17 Prospect Detector
    주어진 위치(point)에서 동, 서, 남, 북 중 한 곳이라도 
    min_prospect_dist(예: 4칸) 이상 벽에 막히지 않는 깊은 시야가 있는지 확인합니다.
    """
    x, y = point
    rows = len(grid)
    cols = len(grid[0])
    
    # 4방향 (상, 하, 좌, 우)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for dx, dy in directions:
        dist = 0
        curr_x, curr_y = x, y
        while 0 <= curr_x < cols and 0 <= curr_y < rows:
            if grid[curr_y][curr_x] == 1: # 벽에 막힘
                break
            dist += 1
            curr_x += dx
            curr_y += dy
            
        # 시작점을 포함해 쟀으므로 1을 빼고 비교
        if (dist - 1) >= min_prospect_dist:
            return True
            
    return False

# =====================================================================
# Step 3: Test Suite (6 Success Cases / 4 Failure Cases)
# =====================================================================

# 5x5 Grid (0: Empty, 1: Wall)
# 0 0 0 0 0
# 0 1 1 1 0
# 0 1 0 1 0
# 0 1 0 0 0
# 0 0 0 0 0
TEST_GRID = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# --- L42 Test Cases ---

def test_l42_success_clear_sight():
    # Success 1: 벽 위쪽의 두 사람
    assert detect_l42_interactional_visibility(TEST_GRID, [(0,0), (4,0)]) is True

def test_l42_success_vertical_sight():
    # Success 2: 오른쪽 통로의 두 사람
    assert detect_l42_interactional_visibility(TEST_GRID, [(4,0), (4,4)]) is True

def test_l42_success_diagonal_sight():
    # Success 3: 바깥쪽 모서리의 두 사람 (벽을 피하는 대각선)
    assert detect_l42_interactional_visibility(TEST_GRID, [(3,4), (4,3)]) is True

def test_l42_failure_blocked_by_wall():
    # Failure 1: 벽을 사이에 둔 두 사람 (위쪽과 안쪽)
    assert detect_l42_interactional_visibility(TEST_GRID, [(2,0), (2,2)]) is False

def test_l42_failure_one_person():
    # Failure 2: 사람이 혼자라 상호작용 불가능
    assert detect_l42_interactional_visibility(TEST_GRID, [(0,0)]) is False

# --- L17 Test Cases ---

def test_l17_success_horizontal_prospect():
    # Success 4: 맨 위쪽 행 (길이 4 이상의 시야 확보)
    assert detect_l17_prospect(TEST_GRID, (0,0), min_prospect_dist=4) is True

def test_l17_success_vertical_prospect():
    # Success 5: 왼쪽 첫 열 (길이 4 이상의 시야 확보)
    assert detect_l17_prospect(TEST_GRID, (0,0), min_prospect_dist=4) is True

def test_l17_success_partial_corridor():
    # Success 6: 하단 통로에서 오른쪽으로 깊은 시야
    assert detect_l17_prospect(TEST_GRID, (0,4), min_prospect_dist=4) is True

def test_l17_failure_inside_room():
    # Failure 3: 좁은 방 안 (문이 열려있지만 시야가 3칸 이상 나오지 않음)
    assert detect_l17_prospect(TEST_GRID, (2,2), min_prospect_dist=3) is False

def test_l17_failure_facing_wall_closely():
    # Failure 4: 벽 바로 앞에 서 있어서 요구 조건을 만족 못함
    assert detect_l17_prospect(TEST_GRID, (2,0), min_prospect_dist=4) is False
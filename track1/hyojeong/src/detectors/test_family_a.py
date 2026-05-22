import math
from typing import List, Dict, Any

# =====================================================================
# Step 2: Typed Contract & Function Signatures
# =====================================================================

def detect_l49_small_group_support(furniture: List[Dict[str, Any]], max_dist: float = 2.5) -> bool:
    """
    L49 SmallGroup-Support Detector
    Determines if seating furniture (chairs, couches) forms a tight cluster 
    of 3 to 5 seats to facilitate small group interaction.
    """
    # 1. 앉을 수 있는 좌석 가구(chair, couch)만 필터링
    seating = [f for f in furniture if f.get("type") in ["chair", "couch"]]
    n = len(seating)
    if n < 3:
        return False

    # 2. 인접 행렬(Adjacency Matrix) 생성: 거리 계산 후 임계값(max_dist) 이내면 연결
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            pos1 = seating[i]["position"]
            pos2 = seating[j]["position"]
            dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
            if dist <= max_dist:
                adj[i].add(j)
                adj[j].add(i)

    # 3. BFS/DFS 알고리즘을 사용해 연결된 가구 그룹(Connected Components) 찾기
    visited = set()
    for i in range(n):
        if i not in visited:
            cluster = []
            queue = [i]
            visited.add(i)
            while queue:
                curr = queue.pop(0)
                cluster.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            # 클러스터 크기가 3개 이상 5개 이하인 그룹이 하나라도 있다면 만족
            if 3 <= len(cluster) <= 5:
                return True
                
    return False


def detect_l44_sociopetal_seating(furniture: List[Dict[str, Any]], max_dist: float = 3.0) -> bool:
    """
    L44 Sociopetal Seating Detector
    Determines if at least one pair of seating furniture faces each other 
    within a conversational distance to encourage face-to-face interaction.
    """
    seating = [f for f in furniture if f.get("type") in ["chair", "couch"]]
    n = len(seating)
    if n < 2:
        return False

    # 모든 두 좌석 쌍(Pair)을 검사
    for i in range(n):
        for j in range(i + 1, n):
            pos1 = seating[i]["position"]
            pos2 = seating[j]["position"]
            
            # 1. 두 좌석 간의 거리 계산
            dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
            if dist > max_dist:
                continue

            # 2. 두 좌석의 방향 벡터(Orientation) 추출
            ori1 = seating[i].get("orientation", [0.0, 0.0])
            ori2 = seating[j].get("orientation", [0.0, 0.0])

            # 1번 좌석에서 2번 좌석을 바라보는 벡터 (v12) 계산 및 정규화
            v12 = [pos2[0] - pos1[0], pos2[1] - pos1[1]]
            len12 = math.sqrt(v12[0]**2 + v12[1]**2)
            if len12 == 0: continue
            v12 = [v12[0]/len12, v12[1]/len12]

            # 2번 좌석에서 1번 좌석을 바라보는 벡터 (v21) 계산 및 정규화
            v21 = [-v12[0], -v12[1]]

            # 3. 내적(Dot Product)을 이용해 방향성 검증
            # 가구의 시선 벡터와 가구 간 상대 벡터의 내적이 0.5 이상이면 서로를 향해 마주 보고 있다고 판단 (약 60도 이내)
            dot1 = ori1[0] * v12[0] + ori1[1] * v12[1]
            dot2 = ori2[0] * v21[0] + ori2[1] * v21[1]

            if dot1 > 0.5 and dot2 > 0.5:
                return True

    return False


# =====================================================================
# Step 3: Test Suite (6 Success Cases / 4 Failure Cases)
# =====================================================================

# --- L49 Test Cases ---

def test_l49_success_perfect_triangle():
    """Success Case 1: 3 chairs arranged in a close triangle (Cluster size = 3)."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0]},
        {"type": "chair", "position": [1.0, 0.0]},
        {"type": "chair", "position": [0.5, 0.86]}
    ]
    assert detect_l49_small_group_support(mock_furniture) is True

def test_l49_success_four_seats():
    """Success Case 2: A couch and two chairs forming a conversational quad (Cluster size = 4)."""
    mock_furniture = [
        {"type": "couch", "position": [0.0, 0.0]},
        {"type": "chair", "position": [1.5, 0.0]},
        {"type": "chair", "position": [0.0, 1.5]},
        {"type": "table", "position": [5.0, 5.0]} # Non-seating should be ignored
    ]
    assert detect_l49_small_group_support(mock_furniture) is True

def test_l49_success_five_seats_line():
    """Success Case 3: 5 chairs chained together closely (Cluster size = 5)."""
    mock_furniture = [{"type": "chair", "position": [float(i), 0.0]} for i in range(5)]
    assert detect_l49_small_group_support(mock_furniture) is True

def test_l49_failure_too_few_seats():
    """Failure Case 1: Only 2 chairs available (Cluster size < 3)."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0]},
        {"type": "chair", "position": [1.0, 1.0]}
    ]
    assert detect_l49_small_group_support(mock_furniture) is False

def test_l49_failure_scattered_chairs():
    """Failure Case 2: 4 chairs but they are too far apart to form a single cluster."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0]},
        {"type": "chair", "position": [10.0, 0.0]},
        {"type": "chair", "position": [0.0, 10.0]},
        {"type": "chair", "position": [10.0, 10.0]}
    ]
    assert detect_l49_small_group_support(mock_furniture) is False


# --- L44 Test Cases ---

def test_l44_success_perfect_facing():
    """Success Case 4: Two chairs directly facing each other within 2 meters."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0], "orientation": [1.0, 0.0]},  # Looking Right
        {"type": "chair", "position": [2.0, 0.0], "orientation": [-1.0, 0.0]}  # Looking Left
    ]
    assert detect_l44_sociopetal_seating(mock_furniture) is True

def test_l44_success_angled_facing():
    """Success Case 5: Two chairs slightly angled but still facing each other."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0], "orientation": [0.707, 0.707]},
        {"type": "chair", "position": [1.5, 1.5], "orientation": [-0.707, -0.707]}
    ]
    assert detect_l44_sociopetal_seating(mock_furniture) is True

def test_l44_success_couch_and_chair():
    """Success Case 6: A couch facing a chair close by."""
    mock_furniture = [
        {"type": "couch", "position": [0.0, 1.0], "orientation": [0.0, -1.0]}, # Looking Down
        {"type": "chair", "position": [0.0, -0.5], "orientation": [0.0, 1.0]}  # Looking Up
    ]
    assert detect_l44_sociopetal_seating(mock_furniture) is True

def test_l44_failure_parallel_looking_away():
    """Failure Case 3: Two chairs side-by-side looking in the same direction (Horizontal/Side layout)."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0], "orientation": [0.0, 1.0]},
        {"type": "chair", "position": [1.0, 0.0], "orientation": [0.0, 1.0]}
    ]
    assert detect_l44_sociopetal_seating(mock_furniture) is False

def test_l44_failure_too_far_apart():
    """Failure Case 4: Chairs face each other but the distance is 15 meters (too far for conversation)."""
    mock_furniture = [
        {"type": "chair", "position": [0.0, 0.0], "orientation": [1.0, 0.0]},
        {"type": "chair", "position": [15.0, 0.0], "orientation": [-1.0, 0.0]}
    ]
    assert detect_l44_sociopetal_seating(mock_furniture) is False
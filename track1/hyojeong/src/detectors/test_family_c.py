import math
from typing import List, Dict, Tuple, Set

# =====================================================================
# Step 2 & 4: Typed Contract & Actual Implementation (Family C)
# =====================================================================

def detect_l57_disengagement_ease(nodes: Dict[int, Tuple[float, float]], 
                                  edges: Dict[int, List[Tuple[int, float]]], 
                                  social_node: int, 
                                  exit_nodes: Set[int]) -> bool:
    """
    L57 Disengagement Ease Detector
    소셜 노드(모임 장소)에서 출구(exit_nodes)로 향하는 서로 다른 독립적인 탈출 경로가 
    2개 이상 존재하는지 확인하여, 분위기를 깨지 않고 자연스럽게 이탈할 수 있는지 평가합니다.
    """
    if social_node not in nodes:
        return False
        
    successful_exit_paths = 0
    
    # 소셜 노드와 직접 연결된 이웃 노드들을 각각의 탈출로 시작점으로 간주
    for neighbor, _ in edges.get(social_node, []):
        queue = [neighbor]
        visited = {social_node, neighbor} # 소셜 노드로 다시 돌아오는 것은 금지
        can_exit = False
        
        # BFS 탐색으로 출구 도달 가능성 확인
        while queue:
            curr = queue.pop(0)
            if curr in exit_nodes:
                can_exit = True
                break
                
            for next_node, _ in edges.get(curr, []):
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)
        
        if can_exit:
            successful_exit_paths += 1
            
    # 독립적인 탈출로가 2개 이상이면 자연스러운 이탈 가능 (True)
    return successful_exit_paths >= 2


def detect_l47_turn_taking_support(nodes: Dict[int, Tuple[float, float]], 
                                   edges: Dict[int, List[Tuple[int, float]]], 
                                   min_width: float = 1.5, 
                                   min_length: float = 3.0) -> bool:
    """
    L47 Turn-Taking Support Detector
    두 사람이 나란히 걸으며 대화할 수 있도록, 통로 너비(1.5m 이상)와 
    길이(3.0m 이상)를 동시에 만족하는 동선 구간이 최소 1개 이상 존재하는지 확인합니다.
    """
    for u, neighbors in edges.items():
        if u not in nodes: continue
        pos_u = nodes[u]
        
        for v, width in neighbors:
            if v not in nodes: continue
            
            # 너비 조건 통과 확인
            if width >= min_width:
                pos_v = nodes[v]
                # 길이(유클리드 거리) 계산
                length = math.sqrt((pos_u[0] - pos_v[0])**2 + (pos_u[1] - pos_v[1])**2)
                
                # 길이 조건도 통과하면 나란히 걷기 좋은 동선 존재
                if length >= min_length:
                    return True
    return False

# =====================================================================
# Step 3: Test Suite (6 Success Cases / 4 Failure Cases)
# =====================================================================

# --- L57 Test Cases ---

def test_l57_success_two_exits():
    # Success 1: 양쪽으로 갈라져서 서로 다른 출구로 나갈 수 있음
    nodes = {1: (0,0), 2: (1,0), 3: (-1,0), 4: (2,0), 5: (-2,0)}
    edges = {1: [(2, 1.0), (3, 1.0)], 2: [(4, 1.0)], 3: [(5, 1.0)]}
    assert detect_l57_disengagement_ease(nodes, edges, social_node=1, exit_nodes={4, 5}) is True

def test_l57_success_multiple_exits():
    # Success 2: 3갈래의 탈출로가 존재
    nodes = {1: (0,0), 2: (1,0), 3: (-1,0), 4: (0,1), 5: (2,0), 6: (-2,0), 7: (0,2)}
    edges = {1: [(2,1.0), (3,1.0), (4,1.0)], 2: [(5,1.0)], 3: [(6,1.0)], 4: [(7,1.0)]}
    assert detect_l57_disengagement_ease(nodes, edges, social_node=1, exit_nodes={5, 6, 7}) is True

def test_l57_success_shared_exit_different_paths():
    # Success 3: 출구는 하나(4번)지만, 그곳으로 가는 길이 두 갈래로 나뉘어 있음
    nodes = {1: (0,0), 2: (0,1), 3: (1,0), 4: (1,1)}
    edges = {1: [(2,1.0), (3,1.0)], 2: [(4,1.0)], 3: [(4,1.0)]}
    assert detect_l57_disengagement_ease(nodes, edges, social_node=1, exit_nodes={4}) is True

def test_l57_failure_single_choke_point():
    # Failure 1: 출구로 가려면 무조건 2번 노드(외길)를 거쳐야 함
    nodes = {1: (0,0), 2: (1,0), 3: (2,0)}
    edges = {1: [(2, 1.0)], 2: [(3, 1.0)]}
    assert detect_l57_disengagement_ease(nodes, edges, social_node=1, exit_nodes={3}) is False

def test_l57_failure_no_exit_path():
    # Failure 2: 나가는 길이 아예 출구와 연결되어 있지 않음
    nodes = {1: (0,0), 2: (1,0), 3: (-1,0)}
    edges = {1: [(2, 1.0), (3, 1.0)]} 
    assert detect_l57_disengagement_ease(nodes, edges, social_node=1, exit_nodes={4}) is False


# --- L47 Test Cases ---

def test_l47_success_wide_long_corridor():
    # Success 4: 너비 2.0, 길이 4.0인 넓고 긴 복도
    nodes = {1: (0,0), 2: (4,0)} 
    edges = {1: [(2, 2.0)]} 
    assert detect_l47_turn_taking_support(nodes, edges, min_width=1.5, min_length=3.0) is True

def test_l47_success_diagonal_wide_corridor():
    # Success 5: 대각선 방향의 길이 5.0, 너비 1.6인 복도
    nodes = {1: (0,0), 2: (3,4)} 
    edges = {1: [(2, 1.6)]} 
    assert detect_l47_turn_taking_support(nodes, edges, min_width=1.5, min_length=3.0) is True

def test_l47_success_complex_graph_has_one_good_path():
    # Success 6: 여러 경로 중 하나가 조건(너비 1.8, 길이 4.0)을 만족함
    nodes = {1: (0,0), 2: (1,0), 3: (5,0)}
    edges = {1: [(2, 1.0)], 2: [(3, 1.8)]} 
    assert detect_l47_turn_taking_support(nodes, edges, min_width=1.5, min_length=3.0) is True

def test_l47_failure_wide_but_too_short():
    # Failure 3: 너비는 2.0으로 넓지만, 길이가 2.0이라 너무 짧음
    nodes = {1: (0,0), 2: (2,0)} 
    edges = {1: [(2, 2.0)]} 
    assert detect_l47_turn_taking_support(nodes, edges, min_width=1.5, min_length=3.0) is False

def test_l47_failure_long_but_too_narrow():
    # Failure 4: 길이는 4.0으로 길지만, 너비가 1.0이라 좁아서 나란히 걷기 힘듦
    nodes = {1: (0,0), 2: (4,0)} 
    edges = {1: [(2, 1.0)]} 
    assert detect_l47_turn_taking_support(nodes, edges, min_width=1.5, min_length=3.0) is False
import numpy as np

# Define constant for unreachable nodes
Z = -1


# Help functions
def ucs_get_item_with_lowest_value(arr):
    min_index = None
    min_middle_value = float('inf') 

    for i, item in enumerate(arr):
        middle_value = item[1]
        if middle_value < min_middle_value:
            min_index = i
            min_middle_value = middle_value

    return min_index

def ucs_matrix_max_width_and_height(matrix):
    max_width = 0
    max_height = len(matrix)  # Initialize max_height with the number of rows

    for row in matrix:
        width = len(row)
        if width > max_width:
            max_width = width

        for col in row:
            if isinstance(col, list):  # Check if the element is a list
                height = len(col)
                if height > max_height:
                    max_height = height

    return max_width, max_height

def ucs_add_to_open_list(x, y, open_list, closed_list, matrix, oldVal, parent):
    # Check x, y
    tmpMatrix = matrix
    max_width, max_height = ucs_matrix_max_width_and_height(tmpMatrix)
    if x < 0 or x > max_width - 1 or y < 0 or y > max_height - 1:
        return

    # Check Z
    if matrix[x][y] == Z:
        return

    # Check if it is in closed_list
    for item in closed_list:
        if item[0] == [x, y]:
            return

    # Add to open list
    open_list.append([[x,y],matrix[x][y]+oldVal,parent])

def ucs_find_position(closed_list, coordinates):
    for i, item in enumerate(closed_list):
        if item[0] == coordinates:
            return i
    return None  # Return None if coordinates are not found

def ucs_remove_duplicates_with_higher_middle_value(nodes):
    unique_nodes = []

    for node in nodes:
        # Check if node has the same beginning as any node already in unique_nodes
        found = False
        for i, unique_node in enumerate(unique_nodes):
            if node[0] == unique_node[0]:
                # If middle value of node is lower, replace the corresponding node in unique_nodes
                if node[1] < unique_node[1]:
                    unique_nodes[i] = node
                found = True
                break

        # If node not found in unique_nodes, add it
        if not found:
            unique_nodes.append(node)

    return unique_nodes

def ucs_print_nodes(nodes):
    printed_nodes = ", ".join("({}, {}, {})".format(str(node[0]), node[1], str(node[2]) if node[2] is not None else "[null]") for node in nodes)
    print(printed_nodes)

def ucs_print_route_backwards(start, end, closed_list):
    route = [end[0]]  # Start with the end node in the route

    print("\n\n\nROUTE:")
    # Backtrack from the end node until reaching the start node
    cnt = 0
    tmpParentCoordinations = end

    while True:
        if tmpParentCoordinations[0] == start:
            break
        
        position = ucs_find_position(closed_list, tmpParentCoordinations[2])
        route.append(closed_list[position][0])
        tmpParentCoordinations = closed_list[position]

        cnt = cnt + 1

    route = route[::-1]
    print(route)

#
#   Uniform Cost Search with closed list
#
def ucs(matrix, start, end):
    open_list = []
    closed_list = []

    # Transpose matrix
    matrix = [list(row) for row in zip(*matrix)]

    # Add the start node to the open list along with its cost
    open_list.append([start, 0, None])

    # Repeat until there are nodes to explore
    cnt = 0
    while open_list:
        # Print iteration
        print("-----------------------------------\n")
        print("---  ", cnt, " iteration ---\n")
        print("-----------------------------------\n")
        print("Open: ")
        ucs_print_nodes(open_list)
        print("Close: ")
        ucs_print_nodes(closed_list)

        # Find lowest
        lowest_item = ucs_get_item_with_lowest_value(open_list)

        # Check if it is final
        if open_list[lowest_item][0] == end:
            ucs_print_route_backwards(start, open_list[lowest_item], closed_list)
            return True

        # Expand nodes
        ucs_add_to_open_list(open_list[lowest_item][0][0] - 1, open_list[lowest_item][0][1] - 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0], open_list[lowest_item][0][1] - 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0] + 1, open_list[lowest_item][0][1] - 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0] - 1, open_list[lowest_item][0][1], open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0] + 1, open_list[lowest_item][0][1], open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0] - 1, open_list[lowest_item][0][1] + 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0], open_list[lowest_item][0][1] + 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])
        ucs_add_to_open_list(open_list[lowest_item][0][0] + 1, open_list[lowest_item][0][1] + 1, open_list, closed_list, matrix, open_list[lowest_item][1], open_list[lowest_item][0])

        # Add to closed_list and remove from open_list
        closed_list.append([open_list[lowest_item][0], open_list[lowest_item][1], open_list[lowest_item][2]])
        open_list.pop(lowest_item)

        # Remove multiple nodes
        open_list = ucs_remove_duplicates_with_higher_middle_value(open_list)

        # Increase counter
        cnt = cnt + 1
     
    # If no path is found
    return False
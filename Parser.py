"""
TODO
- Sort by alpha (DisplayName)
- Presentable
    - Remove colour codes (from lore esp)
    - Remove useless text
- Import group of files
"""
dict = {}
with open("Test Files/gifts.conf", "r", encoding='utf-8') as File1:
    file_contents=File1.read().split(sep="\n")
with open("Test Files/dict.txt", "r", encoding='utf-8') as File2:
    lines = File2.read().split("\n")
for line in lines:
    elem = line.split(";")
    dict[elem[0]] = [elem[1]]
for line in file_contents:
    if line.startswith("#"):  # Removes lines with comments
        file_contents.remove(line)
    elif line == "\n" or line == "}":
        file_contents.remove(line)
map = []
for i in range(len(file_contents)):
    if not file_contents[i].startswith(" ") and not file_contents[i].startswith("\t"): # Finds places where new gifts start
        map.append(i)
individual_gifts = [[] for _ in range(len(map))]
k = 0
for set in individual_gifts:  # Adds all lines from start of gift up until where the next gift starts
    if k + 1 < len(map):
        set.append(file_contents[map[k]:map[k+1]])
        k += 1
    else:
        individual_gifts[k].append(file_contents[map[k]::])
while [""] in individual_gifts:
    individual_gifts.remove([""])  # Removes empty lists caused by 0 indent {'s

# Hotfix
individual = []
for set in individual_gifts:
    individual.append(set[0])
while [""] in individual:
    individual.remove([""])
for set in individual:
    while [""] in set:
        set.remove([""])
"""
Parse Code
------------------------------------------------------------------------------------------------------------------------

Formatting Code
"""
rewards=[]


def find_index(str, oneindex):
    l = []
    for i in range(len(individual[u])):
        if str in individual[u][i]:
            if i not in l:
                l.append(i)
    # l = [individual[u].index(i) for i in individual[u] if str in i]
    if not l:
        return False
    elif oneindex:
        return l[0]
    else:
        return l


def find_node(str, oneindex):
    l = []
    for i in range(len(individual[u])):
        if str in individual[u][i]:
            if i not in l:
                if "0" in individual[u][i]:
                    l.append([i, True])
                else:
                    l.append([i, False])
    # l = [individual[u].index(i) for i in individual[u] if str in i]
    if not l:
        return False
    elif oneindex:
        return l[0][0]
    else:
        return l



def find_index_node(str, oneindex):
    l = [node.index(i) for i in node if str in i]
    if not l:
        return False
    elif oneindex:
        return l[0]
    else:
        return l


for u in range(len(individual)):
    print(u)
    internal_name = individual[u][0].split(" ")[0]
    display_name = individual[u][find_index('displayName', True)].split("displayName=")[1]
    icon = individual[u][find_index('itemType', True)].split("itemType=")[1]
    lores = individual[u][find_index('lores=[', True) + 1:find_index(']', True)]
    print(internal_name)

    # Pools
    """
    Pools start at node 0 and work their way up to node `n`
    Hence, every zero it encounters means that a new pool has started
    """
    pools = len(find_index('"0" {', False))  # Returns number of pools
    chancesum = 0
    pool_info = [[] for _ in range(pools)]
    node_num = 0
    k = 0
    q = 0
    nodes = find_node('" {', False)
    for n in range(len(nodes)):
        if n == len(nodes) - 1:
            pool_info[q].append(individual[u][nodes[n][0]:find_index("type=", True)])
        else:
            pool_info[q].append(individual[u][nodes[n][0]:nodes[n + 1][0]])
            if nodes[n + 1][1] and pools > 1:
                q += 1
        # while True:
        #     print(individual[u][find_index(f'"{node_num}" ', False)[j]:find_index(f'"{node_num+1}" ', False)[j]])
        #     pool_info.append(individual[u][find_index(f'"{node_num}" ', False)[j]:find_index(f'"{node_num+1}" ', False)[j]])
        #     node_num += 1
        #     if "}" in individual[u][find_index("reward=", False)[j] + 1] and "}" in individual[u][find_index("reward=", False)[j] + 2]:
        #         break
        # if j == len(find_index('"0" {', False)):
        #     pool_info.append(individual[u][find_index(f'"{node_num}" ', False)[j]:find_index('type=', True)])
        # else:
        #     pool_info.append(individual[u][find_index(f'"{node_num}" ', False)[j]:find_index('"0" {', False)[j+1] - 1])
        #     print(individual[u][find_index(f'"{node_num}" ', False)[j]:find_index('"0" {', False)[j+1] - 1])
        #     print(find_index('"0" {', False)[j+1])
    rewards = []
    j = 0
    for pool in pool_info:
        rewards.append([[]])
        for node in pool:
            reward = False
            chance = False
            for line in node:
                if "reward=" in line:
                    reward = True
                elif "chance=" in line:
                    chance=True
            for line in node:
                if "reward=" in line:
                    rewards[j][0].append(line.split("=")[1])
                elif "chance=" in line:
                    chancesum += int(line.split("=")[1])
                    rewards[j][0].append(int(line.split("=")[1]))
            if not chance:
                chancesum += 1
                rewards[j][0].insert(-1, 1)
            if not reward:
                rewards[j][0].append("Fail")
        rewards[j].insert(0, chancesum)
        j += 1
        chancesum = 0
        pool_info = []
        node_num = 0
        k = 0
        # print("-------")
        #     for node in pool:
        #         print(node)
        #         if find_index_node("reward=", True):
        #             rewards[j].append(node[find_index_node("reward=", True)].split("=")[1])
        #         else:
        #             rewards[j].append(["Fail"])
        #         if find_index_node("chance=", True):
        #             chancesum += int(node[find_index_node("chance=", True)].split("=")[1])
        #             rewards[j][k].append(int(node[find_index_node("chance=", True)].split("=")[1]))
        #         else:
        #             chancesum += 1
        #             rewards[j][k].append(1)
        #         k += 1
        #     rewards[j].insert(0, chancesum)
        #     print(rewards)
        #     chancesum = 0
        #     pool_info = []
        #     node_num = 0
        #     k = 0
    """
    ------------------------------------------------------------------------------------------------------------------------
    Output
    """
    # with open("Test Files/dict.txt", "a") as dictionary:
    #     dictionary.write(f'{internal_name};{display_name.split("&")[1][1:-1]}\n')
    with open("output.txt", "a") as output:
        output.write(f'\n\n### {internal_name}\n\n'
                     f'<details>\n'
                     f'<summary>Gift Details:</summary>\n'
                     f'Internal Name: {internal_name}\n\n')
        output.write(f"<details>"
                     f"<summary>Gift Contents:</summary>")
        for i in range(pools):
            output.write(f'\nPool {i}\n\n')
            for m in range(1, len(rewards[i][1]) + 1, 2):
                if "giftplayer" in rewards[i][1][m]:
                    if dict.get(rewards[i][1][m].split("%p%")[1][1:-1]):
                        output.write(
                            f"\tReward: {dict[rewards[i][1][m].split('%p%')[1][1:-1]]} ({((rewards[i][1][m - 1] / rewards[i][0]) * 100):.2f}%)\n\n"
                        )
                    elif rewards[i][1][m][-2] in "1234567890" and dict.get(rewards[i][1][m].split("%p%")[1][1:-3]):
                        output.write(
                            f"\tReward: {rewards[i][1][m][-2]}x {dict[rewards[i][1][m].split('%p%')[1][1:-3]]} ({((rewards[i][1][m - 1] / rewards[i][0]) * 100):.2f}%)\n\n"
                        )
                    else:
                        output.write(
                            f"\tReward: {rewards[i][1][m]} ({((rewards[i][1][m - 1] / rewards[i][0]) * 100):.2f}%)\n\n"
                        )
                else:
                    output.write(
                        f"\tReward: {rewards[i][1][m]} ({((rewards[i][1][m - 1] / rewards[i][0]) * 100):.2f}%)\n\n"
                    )
        output.write(f"</details>\n"
                     f"</details>")
    rewards=[]


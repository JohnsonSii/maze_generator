import random
from matplotlib import pyplot as plt
from matplotlib import patches


"""
    初始化数组
    输入: 规模 scale
    输出: 生成好的数组 maze, 待绘制矩形的边长 1 / scale
"""
def array_init(scale):
    return [[(lambda x: (x+1)%2)(i) for i in range(scale - 1)] if j%2 else [1]*(scale - 1) for j in range(scale - 1)], 1 / scale


"""
    通过数组数据绘制网格图形
    输入: maze 数组
"""
def draw_from_data(maze):
    # 遍历数组
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 2:
                draw_grid(row * step, col * step)  # 调用绘制矩形函数



"""
    通过深度优先算法，根据初始化数组生成对应规模的迷宫
    输入: maze 数组
    输出: 处理后的 maze 数组
"""
def generate_deep(maze):
    # 使用 list 数据类型，是因为 list 具有栈的结构，先入后出

    start = (1, 1)
    lst = [start]

    while lst:
        flag = 0
        now = lst[-1]
        row, col = now
        maze[row][col] = 2
        direction = []
        road = []

        for i in range(len(maze)):
            if 0 in maze[i]:
                flag = 1
        if flag == 0:
            break
            
       
        if 0 < row - 2 < scale and maze[row - 2][col] == 0:
            direction.append((row - 2, col))
            road.append((row - 1, col))
        if 0 < col + 2 < scale and maze[row][col + 2] == 0:
            direction.append((row, col + 2))
            road.append((row, col + 1))
        if 0 < row + 2 < scale and maze[row + 2][col] == 0:
            direction.append((row + 2, col))
            road.append((row + 1, col))
        if 0 < col - 2 < scale and maze[row][col - 2] == 0:
            direction.append((row, col - 2))
            road.append((row, col - 1))
  

        if direction == []:
            lst.pop()  # 弹栈
            continue

        dire = random.choice(direction)
        roa = road[direction.index(dire)]
        maze[roa[0]][roa[1]] = 2
        lst.append(dire)

    return maze

"""
    Matplotlib用于绘制矩形的方法
    输入: x, y 坐标
    实现: 在 x, y 位置绘制一个边长为 step, step 的矩形
"""
def draw_grid(x, y):
    ax.add_patch(
        patches.Rectangle(
            (x, y),  # 坐标
            step,  # 宽
            step,  # 高
            facecolor ='white'  # 颜色为白色
        )
    )


if __name__ == '__main__':
    scale = 101  # 迷宫规模，使用奇数
    plt.rcParams['axes.facecolor']='black'  # 设定背景颜色为黑色
    fig = plt.figure()  # 实例一个画布
    ax = fig.add_subplot(111, aspect='equal')  # 添加一个子图，1行 1列 第 1个，纵横比为 相等
    ax.axes.xaxis.set_visible(False)  # 去掉 x轴刻线
    ax.axes.yaxis.set_visible(False)  # 去掉 y轴刻线
    maze, step = array_init(scale)  # 调用数组初始化函数，生成一个网格化数组，类似于：

    # 1代表墙，0代表路
    """
    1  1  1  1  1
    1  0  1  0  1
    1  1  1  1  1
    1  0  1  0  1
    1  1  1  1  1
    """

    maze = generate_deep(maze)  # 调用生成迷宫的函数，深度优先算法
    draw_from_data(maze)  # 调用通过数组数据绘制网格图形的函数
    plt.show()
    
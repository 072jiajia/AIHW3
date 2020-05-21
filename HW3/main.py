from MineSweeperGame import *


def main():
    a = MineSweeperGame((9, 9), 10, 9)
    a = MineSweeperGame((16, 16), 25, 16)
    a = MineSweeperGame((30, 16), 99, 22)

    b = Solver(show=True, show_steps=True)
    print(b.solve(a))
    plt.pause(10)


if __name__ == "__main__":
    main()

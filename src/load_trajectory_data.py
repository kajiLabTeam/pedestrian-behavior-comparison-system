import pandas as pd
import matplotlib.pyplot as plt


def load_trajectory_data(file_path):
    df_trajectory = pd.read_csv(file_path)

    # 描画
    plt.subplots_adjust(hspace=0.3)
    fig = plt.figure(figsize=(10, 10))

    # stay=True と stay=False のデータに分割
    stay_true = df_trajectory[df_trajectory["stay"] == True]
    stay_false = df_trajectory[df_trajectory["stay"] == False]

    plt.scatter(
        stay_false["x"],
        stay_false["y"],
        c="blue",
        s=40,
        label="stay = False (移動中)",
        zorder=2,
    )
    plt.scatter(
        stay_true["x"],
        stay_true["y"],
        c="red",
        s=40,
        label="stay = True (滞在中)",
        zorder=3,
    )

    plt.gca().set_aspect("equal", adjustable="box")
    plt.title("歩行軌跡 (滞在状況で色分け)")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid(True)
    plt.legend()
    plt.close(fig)
    # plt.show()
    return df_trajectory

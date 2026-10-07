import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


# =========================================================
# ค่าเริ่มต้นของข้อมูล Graph ทั้ง 9
# ผู้ใช้สามารถแก้ข้อมูลทั้งหมดจาก GUI ได้
# =========================================================

default_data = [
    {
        "title": "ยอดขายสินค้า",
        "xlabel": "เดือน",
        "ylabel": "ยอดขาย",
        "xdata": "Jan,Feb,Mar,Apr,May",
        "ydata": "120,150,180,140,220"
    },
    {
        "title": "ยอดขายเปรียบเทียบสาขา",
        "xlabel": "จำนวนสินค้า",
        "ylabel": "ยอดขาย",
        "xdata": "10,20,30,40,50,60,70,80,90,100",
        "ydata": "15,25,20,40,35,55,50,70,65,85"
    },
    {
        "title": "ยอดขายแต่ละแผนก",
        "xlabel": "แผนก",
        "ylabel": "ยอดขาย",
        "xdata": "Electronics,Clothing,Food,Home",
        "ydata": "45000,32000,58000,41000"
    },
    {
        "title": "จำนวนลูกค้าแต่ละวัน",
        "xlabel": "วัน",
        "ylabel": "จำนวนลูกค้า",
        "xdata": "Mon,Tue,Wed,Thu,Fri",
        "ydata": "35,42,38,55,61"
    },
    {
        "title": "ยอดขายรายเดือน",
        "xlabel": "เดือน",
        "ylabel": "ยอดขาย",
        "xdata": "Jan,Feb,Mar,Apr,May,Jun",
        "ydata": "120,150,135,180,210,240"
    },
    {
        "title": "คะแนนก่อนและหลังเรียน",
        "xlabel": "นักเรียน",
        "ylabel": "คะแนน",
        "xdata": "A,B,C,D,E",
        "ydata": "55,62,70,48,80"
    },
    {
        "title": "การกระจายของคะแนน",
        "xlabel": "คะแนน",
        "ylabel": "จำนวนคน",
        "xdata": "45,50,52,55,55,58,60,62,65,65,68,70,72,75,78,80,82,85,88,90",
        "ydata": ""
    },
    {
        "title": "สัดส่วนยอดขายสินค้า",
        "xlabel": "สินค้า",
        "ylabel": "เปอร์เซ็นต์",
        "xdata": "Apples,Bananas,Cherries,Dates",
        "ydata": "35,25,25,15"
    },
    {
        "title": "เปรียบเทียบค่าใช้จ่าย",
        "xlabel": "ประเภทค่าใช้จ่าย",
        "ylabel": "จำนวนเงิน",
        "xdata": "อาหาร,เดินทาง,อุปกรณ์,อื่นๆ",
        "ydata": "3500,1800,2500,1200"
    }
]


# =========================================================
# แปลงข้อมูลจาก GUI
# =========================================================

def parse_data(text):
    return [item.strip() for item in text.split(",") if item.strip()]


def parse_numbers(text):
    try:
        return [float(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError:
        return None


# =========================================================
# สร้างกราฟ
# =========================================================

def plot_graph():

    graphs = []

    for i in range(9):

        title = title_entries[i].get().strip()
        xlabel = xlabel_entries[i].get().strip()
        ylabel = ylabel_entries[i].get().strip()
        xdata_text = xdata_entries[i].get().strip()
        ydata_text = ydata_entries[i].get().strip()

        if not title or not xlabel or not ylabel:
            messagebox.showwarning(
                "ข้อมูลไม่ครบ",
                f"กรุณากำหนด Title, X Label และ Y Label ของ Graph {i + 1}"
            )
            return

        if not xdata_text:
            messagebox.showwarning(
                "ข้อมูลไม่ครบ",
                f"กรุณากำหนด X Data ของ Graph {i + 1}"
            )
            return

        graphs.append({
            "title": title,
            "xlabel": xlabel,
            "ylabel": ylabel,
            "xdata": parse_data(xdata_text),
            "ydata": parse_numbers(ydata_text) if ydata_text else []
        })

    # ตรวจสอบข้อมูลของกราฟที่ต้องใช้ X และ Y
    for i in range(8):
        if i != 6:
            if graphs[i]["ydata"] is None:
                messagebox.showerror(
                    "ข้อมูลผิดพลาด",
                    f"Y Data ของ Graph {i + 1} ต้องเป็นตัวเลขคั่นด้วย comma"
                )
                return

            if len(graphs[i]["xdata"]) != len(graphs[i]["ydata"]):
                messagebox.showerror(
                    "ข้อมูลไม่ตรงกัน",
                    f"Graph {i + 1}: จำนวน X Data และ Y Data ต้องเท่ากัน"
                )
                return

    # Graph 7 เป็น Histogram ใช้ X Data อย่างเดียว
    if len(graphs[6]["xdata"]) == 0:
        messagebox.showerror(
            "ข้อมูลผิดพลาด",
            "Graph 7 ต้องมีข้อมูลสำหรับ Histogram"
        )
        return

    histogram_data = parse_numbers(
        ",".join(graphs[6]["xdata"])
    )

    if histogram_data is None:
        messagebox.showerror(
            "ข้อมูลผิดพลาด",
            "X Data ของ Graph 7 ต้องเป็นตัวเลขเท่านั้น"
        )
        return

    # =====================================================
    # สร้าง 9 Graph
    # =====================================================

    fig, ax = plt.subplots(3, 3, figsize=(17, 11))

    fig.suptitle(
        "My First Chart",
        fontsize=22,
        fontweight="bold"
    )

    # -----------------------------------------------------
    # Graph 1 : Scatter
    # -----------------------------------------------------

    x = parse_numbers(",".join(graphs[0]["xdata"]))

    if x is None:
        # ถ้า X เป็นข้อความ ให้ใช้ลำดับแทน
        x = list(range(1, len(graphs[0]["xdata"]) + 1))

    ax[0, 0].scatter(x, graphs[0]["ydata"])

    ax[0, 0].set_xticks(
        range(len(graphs[0]["xdata"]))
    ) if len(graphs[0]["xdata"]) > 0 else None

    ax[0, 0].set_title(graphs[0]["title"])
    ax[0, 0].set_xlabel(graphs[0]["xlabel"])
    ax[0, 0].set_ylabel(graphs[0]["ylabel"])


    # -----------------------------------------------------
    # Graph 2 : Scatter
    # -----------------------------------------------------

    x = parse_numbers(",".join(graphs[1]["xdata"]))

    if x is None:
        x = list(range(1, len(graphs[1]["xdata"]) + 1))

    ax[0, 1].scatter(x, graphs[1]["ydata"])

    ax[0, 1].set_title(graphs[1]["title"])
    ax[0, 1].set_xlabel(graphs[1]["xlabel"])
    ax[0, 1].set_ylabel(graphs[1]["ylabel"])


    # -----------------------------------------------------
    # Graph 3 : Horizontal Bar
    # -----------------------------------------------------

    ax[0, 2].barh(
        graphs[2]["xdata"],
        graphs[2]["ydata"]
    )

    ax[0, 2].set_title(graphs[2]["title"])
    ax[0, 2].set_xlabel(graphs[2]["xlabel"])
    ax[0, 2].set_ylabel(graphs[2]["ylabel"])


    # -----------------------------------------------------
    # Graph 4 : Bar
    # -----------------------------------------------------

    ax[1, 0].bar(
        graphs[3]["xdata"],
        graphs[3]["ydata"]
    )

    ax[1, 0].set_title(graphs[3]["title"])
    ax[1, 0].set_xlabel(graphs[3]["xlabel"])
    ax[1, 0].set_ylabel(graphs[3]["ylabel"])

    ax[1, 0].tick_params(axis="x", rotation=25)


    # -----------------------------------------------------
    # Graph 5 : Line
    # -----------------------------------------------------

    ax[1, 1].plot(
        graphs[4]["xdata"],
        graphs[4]["ydata"],
        marker="o"
    )

    ax[1, 1].set_title(graphs[4]["title"])
    ax[1, 1].set_xlabel(graphs[4]["xlabel"])
    ax[1, 1].set_ylabel(graphs[4]["ylabel"])


    # -----------------------------------------------------
    # Graph 6 : Line + Marker
    # -----------------------------------------------------

    ax[1, 2].plot(
        graphs[5]["xdata"],
        graphs[5]["ydata"],
        marker="o"
    )

    ax[1, 2].set_title(graphs[5]["title"])
    ax[1, 2].set_xlabel(graphs[5]["xlabel"])
    ax[1, 2].set_ylabel(graphs[5]["ylabel"])


    # -----------------------------------------------------
    # Graph 7 : Histogram
    # -----------------------------------------------------

    ax[2, 0].hist(
        histogram_data,
        bins=8
    )

    ax[2, 0].set_title(graphs[6]["title"])
    ax[2, 0].set_xlabel(graphs[6]["xlabel"])
    ax[2, 0].set_ylabel(graphs[6]["ylabel"])


    # -----------------------------------------------------
    # Graph 8 : Pie Chart แบบในตัวอย่าง
    # -----------------------------------------------------

    ax[2, 1].pie(
        graphs[7]["ydata"],
        labels=graphs[7]["xdata"],
        autopct="%1.1f%%",
        explode=(0.1, 0, 0, 0),
        shadow=True
    )

    ax[2, 1].set_title(graphs[7]["title"])
    ax[2, 1].set_xlabel(graphs[7]["xlabel"])
    ax[2, 1].set_ylabel(graphs[7]["ylabel"])


    # -----------------------------------------------------
    # Graph 9 : Pie Chart
    # -----------------------------------------------------

    ax[2, 2].pie(
        graphs[8]["ydata"],
        labels=graphs[8]["xdata"],
        autopct="%1.1f%%"
    )

    ax[2, 2].set_title(graphs[8]["title"])
    ax[2, 2].set_xlabel(graphs[8]["xlabel"])
    ax[2, 2].set_ylabel(graphs[8]["ylabel"])


    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.show()


# =========================================================
# GUI
# =========================================================

root = tk.Tk()
root.title("My First Chart - Data Analytics")
root.geometry("1200x900")


main_title = tk.Label(
    root,
    text="My First Chart",
    font=("Arial", 22, "bold")
)

main_title.pack(pady=10)


description = tk.Label(
    root,
    text="กำหนดข้อมูลเปรียบเทียบของ Graph ทั้ง 9 ได้จาก GUI",
    font=("Arial", 12)
)

description.pack(pady=5)


# =========================================================
# Frame หลัก
# =========================================================

container = tk.Frame(root)
container.pack(fill="both", expand=True, padx=15, pady=10)


# =========================================================
# เก็บ Entry
# =========================================================

title_entries = []
xlabel_entries = []
ylabel_entries = []
xdata_entries = []
ydata_entries = []


# =========================================================
# สร้าง GUI Graph 1-9
# =========================================================

for i in range(9):

    row = i // 3
    column = i % 3

    frame = tk.LabelFrame(
        container,
        text=f"Graph {i + 1}",
        font=("Arial", 11, "bold"),
        padx=8,
        pady=8
    )

    frame.grid(
        row=row,
        column=column,
        padx=7,
        pady=7,
        sticky="nsew"
    )

    # Title
    tk.Label(
        frame,
        text="Title:"
    ).grid(row=0, column=0, sticky="w", pady=3)

    entry_title = tk.Entry(
        frame,
        width=30
    )

    entry_title.insert(
        0,
        default_data[i]["title"]
    )

    entry_title.grid(
        row=0,
        column=1,
        pady=3
    )

    title_entries.append(entry_title)


    # X Label
    tk.Label(
        frame,
        text="X Label:"
    ).grid(row=1, column=0, sticky="w", pady=3)

    entry_xlabel = tk.Entry(
        frame,
        width=30
    )

    entry_xlabel.insert(
        0,
        default_data[i]["xlabel"]
    )

    entry_xlabel.grid(
        row=1,
        column=1,
        pady=3
    )

    xlabel_entries.append(entry_xlabel)


    # Y Label
    tk.Label(
        frame,
        text="Y Label:"
    ).grid(row=2, column=0, sticky="w", pady=3)

    entry_ylabel = tk.Entry(
        frame,
        width=30
    )

    entry_ylabel.insert(
        0,
        default_data[i]["ylabel"]
    )

    entry_ylabel.grid(
        row=2,
        column=1,
        pady=3
    )

    ylabel_entries.append(entry_ylabel)


    # X Data
    tk.Label(
        frame,
        text="X Data:"
    ).grid(row=3, column=0, sticky="w", pady=3)

    entry_xdata = tk.Entry(
        frame,
        width=30
    )

    entry_xdata.insert(
        0,
        default_data[i]["xdata"]
    )

    entry_xdata.grid(
        row=3,
        column=1,
        pady=3
    )

    xdata_entries.append(entry_xdata)


    # Y Data
    tk.Label(
        frame,
        text="Y Data:"
    ).grid(row=4, column=0, sticky="w", pady=3)

    entry_ydata = tk.Entry(
        frame,
        width=30
    )

    entry_ydata.insert(
        0,
        default_data[i]["ydata"]
    )

    entry_ydata.grid(
        row=4,
        column=1,
        pady=3
    )

    ydata_entries.append(entry_ydata)


# =========================================================
# คำอธิบายการกรอกข้อมูล
# =========================================================

help_text = tk.Label(
    root,
    text=(
        "ใส่ข้อมูลคั่นด้วย comma เช่น X Data: Jan,Feb,Mar "
        "| Y Data: 100,150,200   "
        "สำหรับ Pie Chart: X Data = ชื่อหมวดหมู่, Y Data = ค่า"
    ),
    font=("Arial", 10)
)

help_text.pack(pady=5)


# =========================================================
# ปุ่มสร้างกราฟ
# =========================================================

plot_button = tk.Button(
    root,
    text="PLOT GRAPH",
    font=("Arial", 14, "bold"),
    width=20,
    height=2,
    command=plot_graph
)

plot_button.pack(pady=10)


root.mainloop()

import streamlit as st
from graphviz import Digraph
with st.expander("📄 查看源代码"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
# 颜色常量
RED = "RED"
BLACK = "BLACK"

# 正确初始化的 NIL 节点
class NilNode:
    def __init__(self):
        self.key = None
        self.color = BLACK
        self.left = self
        self.right = self
        self.parent = None

NIL = NilNode()  # 全局 NIL 节点

# 红黑树节点
class RBNode:
    def __init__(self, key):
        self.key = key
        self.color = RED
        self.left = NIL
        self.right = NIL
        self.parent = None

# 红黑树类
class RedBlackTree:
    def __init__(self):
        self.root = NIL

    def insert(self, key):
        new_node = RBNode(key)
        parent = None
        current = self.root

        while current != NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.left = new_node.right = NIL
        new_node.color = RED
        self.fix_insert(new_node)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.rotate_left(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rotate_right(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_left(z.parent.parent)
        self.root.color = BLACK

# 可视化树结构
def draw_tree(node, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle', style='filled')

    if node == NIL or node.key is None:
        return dot  # 遇到 NIL，终止递归

    node_id = str(id(node))
    color = "red" if node.color == RED else "black"
    font_color = "white"
    dot.node(node_id, label=str(node.key), fillcolor=color, fontcolor=font_color)

    for child, side in [(node.left, "L"), (node.right, "R")]:
        if child != NIL and child.key is not None:
            child_id = str(id(child))
            draw_tree(child, dot)
            dot.edge(node_id, child_id)
        else:
            nil_id = f"nil_{id(node)}_{side}"
            dot.node(nil_id, label="NIL", color="gray", fontcolor="gray", shape="circle")
            dot.edge(node_id, nil_id)

    return dot


# Streamlit 界面
st.set_page_config(page_title="红黑树演示", layout="centered")
st.title("🌳 红黑树插入演示")

if "tree" not in st.session_state:
    st.session_state.tree = RedBlackTree()
    st.session_state.inserted = []

user_input = st.text_input("插入整数键（多个用逗号分隔）", "")

if st.button("插入"):
    try:
        keys = [int(x.strip()) for x in user_input.split(",") if x.strip()]
        for k in keys:
            if k not in st.session_state.inserted:
                st.session_state.tree.insert(k)
                st.session_state.inserted.append(k)
    except:
        st.error("⚠️ 请输入合法的整数（如 10 或 5, 8, 3）")

if st.session_state.inserted:
    st.write("🔢 已插入键值：", st.session_state.inserted)
    dot = draw_tree(st.session_state.tree.root)
    st.graphviz_chart(dot)
else:
    st.info("请输入一些整数以构建红黑树。")

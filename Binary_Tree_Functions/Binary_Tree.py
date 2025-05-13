import wx

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def find(self, val):
        return self._find(self.root, val)
    
    def _find(self, node, val):
        if node is None:
            return None  # If the node doesn't exist, return None
        if node.val == val:
            return node  # If found, return the node
        elif val < node.val:
            return self._find(node.left, val)
        else:
            return self._find(node.right, val)

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left:
                self._insert(node.left, val)
            else:
                node.left = TreeNode(val)
        else:
            if node.right:
                self._insert(node.right, val)
            else:
                node.right = TreeNode(val)

    def inorder(self, node, result):
        if node:
            self.inorder(node.left, result)
            result.append(node)
            self.inorder(node.right, result)

    def preorder(self, node, result):
        if node:
            result.append(node)
            self.preorder(node.left, result)
            self.preorder(node.right, result)

class TreePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.bst = BinarySearchTree()
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.node_positions = {}
        self.visiting_node = None
        self.found_node = None  # To store the found node

        # Define a safe light blue color using RGB (cross-platform)
        self.safe_lightblue = wx.Colour(173, 216, 230)
        self.found_color = wx.Colour(255, 0, 0)  # Red color for found node

    def insert_value(self, val):
        self.bst.insert(val)
        self.Refresh()

    def reset_tree(self):
        self.bst = BinarySearchTree()
        self.node_positions.clear()
        self.visiting_node = None
        self.found_node = None  # Reset found node
        self.Refresh()

    def traverse_and_color(self, order='inorder'):
        self.node_positions = {}
        result = []
        if order == 'inorder':
            self.bst.inorder(self.bst.root, result)
        elif order == 'preorder':
            self.bst.preorder(self.bst.root, result)

        delay = 0
        for node in result:
            wx.CallLater(delay, self.color_node, node)
            delay += 500

    def color_node(self, node):
        self.visiting_node = node
        self.Refresh()
        wx.CallLater(400, self.clear_color)

    def clear_color(self):
        self.visiting_node = None
        self.found_node = None  # Clear the found node after coloring
        self.Refresh()

    def find_and_highlight(self, val):
        self.found_node = self.bst.find(val)  # Find the node
        if self.found_node:  # If found, highlight it
            self.Refresh()

    def draw_tree(self, dc, node, x, y, x_offset):
        if node:
            pos = (x, y)
            self.node_positions[node] = pos

            # Set color for the found node
            if node == self.found_node:
                dc.SetBrush(wx.Brush(self.found_color))
            elif node == self.visiting_node:
                dc.SetBrush(wx.Brush("red"))
            else:
                dc.SetBrush(wx.Brush(self.safe_lightblue))  # Use RGB-defined light blue

            dc.SetPen(wx.Pen("black", 1))
            dc.DrawCircle(x, y, 20)
            dc.DrawText(str(node.val), x - 5, y - 5)

            if node.left:
                dc.DrawLine(x, y, x - x_offset, y + 60)
                self.draw_tree(dc, node.left, x - x_offset, y + 60, x_offset // 2)
            if node.right:
                dc.DrawLine(x, y, x + x_offset, y + 60)
                self.draw_tree(dc, node.right, x + x_offset, y + 60, x_offset // 2)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        if self.bst.root:
            self.draw_tree(dc, self.bst.root, self.GetSize()[0] // 2, 40, 100)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Binary Search Tree Visualizer", size=(800, 600))
        self.panel = TreePanel(self)

        self.input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

        btn_inorder = wx.Button(self, label="In-order")
        btn_preorder = wx.Button(self, label="Pre-order")
        btn_reset = wx.Button(self, label="Reset")
        btn_find = wx.Button(self, label="Find")

        btn_inorder.Bind(wx.EVT_BUTTON, lambda e: self.panel.traverse_and_color('inorder'))
        btn_preorder.Bind(wx.EVT_BUTTON, lambda e: self.panel.traverse_and_color('preorder'))
        btn_reset.Bind(wx.EVT_BUTTON, lambda e: self.panel.reset_tree())
        btn_find.Bind(wx.EVT_BUTTON, self.on_find)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_inorder, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(btn_preorder, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(btn_reset, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(btn_find, 1, wx.EXPAND | wx.ALL, 5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.panel, 1, wx.EXPAND)
        vbox.Add(self.input, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.EXPAND)

        self.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_enter(self, event):
        val = self.input.GetValue()
        if val.isdigit():
            self.panel.insert_value(int(val))
            self.input.Clear()

    def on_find(self, event):
        val = self.input.GetValue()
        if val.isdigit():
            self.panel.find_and_highlight(int(val))
            self.input.Clear()



import wx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Binary_Tree_Functions.Binary_Tree import BinarySearchTree, TreeNode, MainFrame

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

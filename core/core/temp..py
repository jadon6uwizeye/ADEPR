#Find the sum of all left leaves in a given binary tree
#A left leaf is a leaf node that is the left child of its parent
#For example, in the following tree there are two left leaves: 9 and 15

#Definition for a binary tree node.
class TreeNode:
   def __init__(self, val=0, left=None, right=None):
         self.val = val
         self.left = left
         self.right = right

class Solution:
   def sumOfLeftLeaves(self, root: TreeNode) -> int:
         if root is None:
            return 0
         if root.left and root.left.left is None and root.left.right is None:
            return root.left.val + self.sumOfLeftLeaves(root.right)
         return self.sumOfLeftLeaves(root.left) + self.sumOfLeftLeaves(root.right)

#Driver code
if __name__ == "__main__":
   root = TreeNode(3)
   root.left = TreeNode(9)
   root.right = TreeNode(20)
   root.right.left = TreeNode(15)
   root.right.right = TreeNode(7)
   print(Solution().sumOfLeftLeaves(root))
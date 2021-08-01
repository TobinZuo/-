[Toc]
## 题目信息
**题目链接**: https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof
<p>给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。</p>

<p><a href="https://baike.baidu.com/item/%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88/8918834?fr=aladdin" target="_blank">百度百科</a>中最近公共祖先的定义为：&ldquo;对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（<strong>一个节点也可以是它自己的祖先</strong>）。&rdquo;</p>

<p>例如，给定如下二叉树:&nbsp; root =&nbsp;[3,5,1,6,2,0,8,null,null,7,4]</p>

<p><img alt="" src="https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/12/15/binarytree.png"></p>

<p>&nbsp;</p>

<p><strong>示例 1:</strong></p>

<pre><strong>输入:</strong> root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
<strong>输出:</strong> 3
<strong>解释: </strong>节点 <code>5 </code>和节点 <code>1 </code>的最近公共祖先是节点 <code>3。</code>
</pre>

<p><strong>示例&nbsp;2:</strong></p>

<pre><strong>输入:</strong> root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
<strong>输出:</strong> 5
<strong>解释: </strong>节点 <code>5 </code>和节点 <code>4 </code>的最近公共祖先是节点 <code>5。</code>因为根据定义最近公共祖先节点可以为节点本身。
</pre>

<p>&nbsp;</p>

<p><strong>说明:</strong></p>

<ul>
	<li>所有节点的值都是唯一的。</li>
	<li>p、q 为不同节点且均存在于给定的二叉树中。</li>
</ul>

<p>注意：本题与主站 236 题相同：<a href="https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/">https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/</a></p>

## Python
### 解题思路
两个节点p和q的最近公共祖先，要么是p或者q本身，要么是某节点node，p和q分别在node的左右（右左）子树中。后序遍历，分别求得左右子树中的最近公共祖先，如果left是空，right不为空，说明最近公共祖先在右子树中，right即为右子树中最近公共祖先。反之，left是左子树中的最近公共祖先。当left和right均不为空，说明p和q在当前节点的左右（右左）子树中，当前节点node即为最近公共祖先，直接返回当前节点node。

递归边界是到达叶子节点要返回，到达p，q要返回。最近公共祖先不会在p和q的子节点中，所以碰到直接返回。
### 复杂度分析
**时间复杂度**：$O(N)$。N为二叉树的节点个数。

**空间复杂度**：$O(h)$。h为树高。递归深度最深为树高。

### 解题代码
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if root is None or root == p or root == q: 
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left is None:
            return right
        elif right is None:
            return left
        else:
            return root
```
## 相似题目
无
## 相关topic
Topic | Link
:-----:|:----:
Tree | https://leetcode-cn.com/problems/tree
Depth-First Search | https://leetcode-cn.com/problems/depth-first-search
Binary Tree | https://leetcode-cn.com/problems/binary-tree
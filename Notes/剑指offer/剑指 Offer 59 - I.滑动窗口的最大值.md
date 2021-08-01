[Toc]
## 题目信息
**题目链接**: https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof
<p>给定一个数组 <code>nums</code> 和滑动窗口的大小 <code>k</code>，请找出所有滑动窗口里的最大值。</p>

<p><strong>示例:</strong></p>

<pre><strong>输入:</strong> <em>nums</em> = <code>[1,3,-1,-3,5,3,6,7]</code>, 和 <em>k</em> = 3
<strong>输出: </strong><code>[3,3,5,5,6,7] 
<strong>解释: 
</strong></code>
  滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7</pre>

<p>&nbsp;</p>

<p><strong>提示：</strong></p>

<p>你可以假设 <em>k </em>总是有效的，在输入数组不为空的情况下，1 &le; k &le;&nbsp;输入数组的大小。</p>

<p>注意：本题与主站 239 题相同：<a href="https://leetcode-cn.com/problems/sliding-window-maximum/">https://leetcode-cn.com/problems/sliding-window-maximum/</a></p>

## Python
### 解题思路
单调栈的思想，使用双端队列。[1, 3, -1]，比如这种窗口，1就不用保存，但是-1需要保存，因为随着窗口右移，3会被弹出，-1可能会成为最大值。双端队列中保存索引。主要是两个操作：

1. 当新来的元素大于队尾元素时，队尾元素不断弹出，直到队列为空或者队尾元素>新来元素。
2. 当队首元素索引已经不在窗口内时，需要弹出。

队首索引指向的元素始终是窗口内最大的元素。
### 复杂度分析
**时间复杂度**：$O(N)$。N为数组nums的大小

**空间复杂度**：$O(k)$。k为窗口大小。

### 解题代码
```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = collections.deque()
        l = len(nums)
        i = 0 
        res = []
        while i < l:
            while len(dq) != 0 and nums[dq[-1]] <= nums[i]:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:
                dq.popleft()
            if i >= k-1:
                res.append(nums[dq[0]])
            i += 1
        return res
```
## 相似题目
无
## 相关topic
Topic | Link
:-----:|:----:
Queue | https://leetcode-cn.com/problems/queue
Sliding Window | https://leetcode-cn.com/problems/sliding-window
Monotonic Queue | https://leetcode-cn.com/problems/monotonic-queue
Heap (Priority Queue) | https://leetcode-cn.com/problems/heap-priority-queue
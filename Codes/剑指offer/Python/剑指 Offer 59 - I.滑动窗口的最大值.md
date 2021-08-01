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
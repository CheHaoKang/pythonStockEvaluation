

#https://leetcode.com/problems/3sum-closest/description/
def threeSumClosest(self, num, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        num.sort()
        result = num[0] + num[1] + num[2]
        for i in range(len(num) - 2):
            j, k = i+1, len(num) - 1
            while j < k:
                sum = num[i] + num[j] + num[k]
                if sum == target:
                    return sum
                
                if abs(sum - target) < abs(result - target):
                    result = sum
                
                if sum < target:
                    j += 1
                elif sum > target:
                    k -= 1
            
        return result

#https://leetcode.com/problems/4sum/description/
def fourSum(self, nums, target):
    def findNsum(nums, target, N, result, results):
        if len(nums) < N or N < 2 or target < nums[0]*N or target > nums[-1]*N:  # early termination
            return
        if N == 2: # two pointers solve sorted 2-sum problem
            l,r = 0,len(nums)-1
            while l < r:
                s = nums[l] + nums[r]
                if s == target:
                    results.append(result + [nums[l], nums[r]])
                    l += 1
                    while l < r and nums[l] == nums[l-1]:
                        l += 1
                elif s < target:
                    l += 1
                else:
                    r -= 1
        else: # recursively reduce N
            for i in range(len(nums)-N+1):
                if i == 0 or (i > 0 and nums[i-1] != nums[i]):
                    findNsum(nums[i+1:], target-nums[i], N-1, result+[nums[i]], results)

    results = []
    findNsum(sorted(nums), target, 4, [], results)
    return results

#https://leetcode.com/problems/generate-parentheses/description/
def generateParenthesis(n):
    def generate(p, left, right, parens=[]):
        if left:
            generate(p + '(', left-1, right)
        if right > left:
            generate(p + ')', left, right-1)
        if right==0:
            parens.append(p)
        return parens
    return generate('', n, n)

#https://leetcode.com/problems/search-in-rotated-sorted-array/description/
    def search(self, nums, target):
        if not nums:
            return -1

        low, high = 0, len(nums) - 1

        while low <= high:
            mid = int((low + high) / 2)
            if target == nums[mid]:
                return mid

            if nums[low] <= nums[mid]:
                if nums[low] <= target <= nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if nums[mid] <= target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1

        return -1

#https://leetcode.com/problems/valid-sudoku/description/
    def isValidSudoku(self, board):
        return (self.is_row_valid(board) and
                self.is_col_valid(board) and
                self.is_square_valid(board))

    def is_row_valid(self, board):
        for row in board:
            if not self.is_unit_valid(row):
                return False
        return True

    def is_col_valid(self, board):
        for col in zip(*board):
            if not self.is_unit_valid(col):
                return False
        return True

    def is_square_valid(self, board):
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not self.is_unit_valid(square):
                    return False
        return True

    def is_unit_valid(self, unit):
        unit = [i for i in unit if i != '.']
        return len(set(unit)) == len(unit)

#https://leetcode.com/problems/merge-intervals/description/
def merge(self, intervals):
    out = []
    for i in sorted(intervals, key=lambda i: i.start):
        if out and i.start <= out[-1].end:
            out[-1].end = max(out[-1].end, i.end)
        else:
            out += i,
    return out


#https://leetcode.com/problems/group-anagrams/description/
def groupAnagrams(self, strs):
    grouped = {}
    for s in strs:
        # print(sorted(s))
        grouped.setdefault(''.join(sorted(s)), []).append(s)
        # grouped[''.join(sorted(s))] = grouped.get(''.join(sorted(s)), []) + [s]

    # print(list(grouped.values()))
    return list(grouped.values())


#https://leetcode.com/problems/multiply-strings/description/
  def multiply(self, num1, num2):
        res = 0
        carry1 = 1
        for n1 in num1[::-1]:
            carry2 = 1
            for n2 in num2[::-1]:
                res += int(n1)*int(n2)*carry1*carry2
                carry2 *= 10
            carry1 *= 10
        return str(res)

#https://leetcode.com/problems/add-two-numbers/description/
    def addTwoNumbers(self, l1, l2):
        carry = 0
        root = n = ListNode(0)
        while l1 or l2 or carry:
            v1 = v2 = 0
            if l1:
                v1 = l1.val
                l1 = l1.next
            if l2:
                v2 = l2.val
                l2 = l2.next
            carry, val = divmod(v1+v2+carry, 10)
            n.next = ListNode(val)
            n = n.next
        return root.next

#https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
    def lengthOfLongestSubstring(self, s):
        used = {}
        max_length = start = 0
        for i, c in enumerate(s):
            print(i, c)
            if c in used and start <= used[c]:
                start = used[c] + 1
            else:
                max_length = max(max_length, i - start + 1)
                
            used[c] = i


        print(used)                
        return max_length


# https://leetcode.com/problems/decode-ways/description/
# v tells the previous number of ways
# w tells the number of ways
# p is the previous digit
# d is the current digit
def numDecodings(self, s):
    v, w, p = 0, int(s>''), ''
    for d in s:
        v, w, p = w, (d>'0')*w + (9<int(p+d)<27)*v, d
    return w
#https://leetcode.com/problems/generate-parentheses/description/
class Solution:
    def validate(self,parenthesis):
        leftParenthesis = 0
        for ch in parenthesis:
            if ch=='(':
                leftParenthesis += 1
            elif ch==')':
                leftParenthesis -= 1

            if leftParenthesis < 0:
                return False,leftParenthesis

        if leftParenthesis >= 0:
            return True,leftParenthesis
        else:
            return False,leftParenthesis

    def generateParenthesisRecursive(self,n, parenthesis, current, answer):
        # print(current)
        TrueFalse, numParenthesis = self.validate(current)
        if TrueFalse:
            if len(current) < n*2:
                self.generateParenthesisRecursive(n, '(', current + parenthesis, answer)
                self.generateParenthesisRecursive(n, ')', current + parenthesis, answer)
            elif len(current) == n*2:
                if numParenthesis==0:
                    if current not in answer:
                        answer.append(current)

    def generateParenthesis(self,n):
        answer = []
        self.generateParenthesisRecursive(n, '(', '', answer)
        return answer
        

#https://leetcode.com/problems/combination-sum/description/
class Solution:
    def combinationSum(self, candidates, target):
        results = []
        self.generateCombination(0, sorted(candidates), [], target, results)
        print(results)
        
        return results
    
    def generateCombination(self, candidateIndex, candidates, nowList, target, results):
        # print(candidateIndex,candidates,nowList,candidates[0])
        for index in range(candidateIndex, len(candidates)):
            if sum(nowList) + candidates[index] == target:
                results.append(nowList + [candidates[index]])
            elif sum(nowList) + candidates[index] < target:
                # print(index, candidates[index], nowList + candidates[index])
                self.generateCombination(index, candidates, nowList + [candidates[index]], target, results)


#https://leetcode.com/problems/permutations/description/#
class Solution:
    def permute(self, nums):
        results = []
        self.generatePermutation(nums, len(nums), [], results)
        print(results)

        return results

    def generatePermutation(self, nums, totalLen, nowNums, results):
        if len(nowNums)==totalLen:
            results.append(nowNums)
        else:
            for oneNum in nums:
                copyNums = copy.copy(nums)
                copyNums.remove(oneNum)
                self.generatePermutation(copyNums, totalLen, nowNums+[oneNum], results)

#https://leetcode.com/problems/group-anagrams/description/
def groupAnagrams(strs):
    """
    :type strs: List[str]
    :rtype: List[List[str]]
    """
    anagramDictionary = {}
    for oneStr in strs:
        chDictionary = {}
        for oneCh in oneStr:
            chDictionary[oneCh] = chDictionary.get(oneCh, 0) + 1
        # print(chDictionary)
        chDictionary = sorted(chDictionary.items(), key=operator.itemgetter(0), reverse=True)
        # print(chDictionary)
        freqStr = ''
        for freqDictionary in chDictionary:
            freqStr += str(freqDictionary[0]) + str(freqDictionary[1])
        # print(freqStr)
        anagramDictionary[freqStr] = anagramDictionary.get(freqStr, []) + [oneStr]
        # print('==========')

    # print(anagramDictionary)
    resultList = []
    for key in anagramDictionary:
        resultList.append(anagramDictionary[key])
    return resultList

#https://leetcode.com/problems/add-two-numbers/description/
class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        head = None
        current = None
        carry = 0
        while l1!=None or l2!=None or carry!=0:
            summand = l1.val if l1 else 0
            addend = l2.val if l2 else 0
            l1 = l1.next if l1!=None else None
            l2 = l2.next if l2!=None else None
                
            ans = ListNode((summand+addend+carry)%10)
            carry = int((summand+addend+carry)/10)

            print(summand, addend, ans.val)
            
            if not head:
                head = current = ans
                # print(current.val)
            else:
                current.next = ans
                current = ans
                # print(current.val)
        
        ansList = []
        while head!=None:
            ansList.append(head.val)
            head = head.next
        
        return ansList


#https://leetcode.com/problems/zigzag-conversion/description/
class Solution:
    def convert(self, s, numRows):
        if numRows==1:
            return s
        
        ans = [[] for i in range(numRows)]
        # print(ans)
        
        onePeriodNum = 2*numRows-2
        for j in range(0, len(s), onePeriodNum):
            for i in range(onePeriodNum):
                if i+j > len(s)-1:
                    break
                
                # print(i, j)
                
                if i > numRows-1:
                    ans[2*numRows-i-2] += [s[i+j]]
                else:
                    ans[i] += [s[i+j]]
            
        ansStr = ''
        for oneList in ans:
            ansStr += ''.join(oneList)
        # print(ansStr)
        
        return ansStr
import itertools

def generatePairs(size):
    result = []
    for p1 in range(size):
        for p2 in range(p1+1,size):
            result.append((p1,p2))
    return result

def correctPair(pair):
    if pair[0] > pair[1]:
        return (pair[1], pair[0])
    else:
        return (pair[0], pair[1])

def generatePermutations(size):
    return list(itertools.permutations(list(range(size))))

#source: https://www.tutorialspoint.com/next-permutation-in-python
def nextPermutation(nums):
    found = False
    i = len(nums)-2
    while i >=0:
        if nums[i] < nums[i+1]:
            found =True
            break
        i-=1
    if not found:
        nums.sort()
    else:
        m = findMaxIndex(i+1,nums,nums[i])
        nums[i],nums[m] = nums[m],nums[i]
        nums[i+1:] = nums[i+1:][::-1]
    return nums

#source: https://www.tutorialspoint.com/next-permutation-in-python
def findMaxIndex(index,a,curr):
    ans = -1
    index = 0
    for i in range(index,len(a)):
        if a[i]>curr:
            if ans == -1:
                ans = curr
                index = i
            else:
                ans = min(ans,a[i])
                index = i
    return index

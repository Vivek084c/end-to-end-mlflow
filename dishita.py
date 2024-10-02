def subsets(nums):
    result = []
    
    def backtrack(start, path):
        # Append the current subset to the result
        # if path:
        #     result.append(path)
        if path==[]:
            pass
        else:
            result.append(path)
        

        #checking the further subset
        for i in range(start, len(nums)):
            backtrack(i+1, path + [nums[i]])
        
    #calling the function
    backtrack(0, [])
    return result


# Example usage
input_array = input()
all_subsets = subsets(input_array.split(" "))
for i in all_subsets:
    print("")
    for j in i:
        print(j," ",sep=" ",end="")

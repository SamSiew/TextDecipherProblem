class Decipher:
    def __init__(self):
        self.message = ""

    def getMessage(self):
        """
        :return: string containing instance message
        Time complexity: O(1), returning a value
        Space complexity: O(m), it requires a bytes to store each character of copy of instance message.
        where m is number of character in string
        """
        return self.message

    def messageFind(self,filename):
        """
        Using dynamic programming to find longest subsequence of two encrypted string.

        :param filename: file that contains two encrypted text
        :return: longest common words in both text
        Time complexity: O(nm), occurs when reading first text and seconds text.
                        No early termination since every character is needed to read
                        and early termination only happens on function retrieving longest subsequence
                        of previous iteration.
        Space complexity: O(nm), no matter what length of two string is, adjency matrix(nm size)is created to
                          store optimal solution of two string.
        where n and m be the size of first text and second text respectively.
        Pre-requisite: files must exist,filecontent must be only two encrypted text
        """
        #read file into list of words
        try:
            filecontent =[]
            with open(filename) as file:
                for line in file:
                    filecontent.append(line.strip())
                file.close()
            if len(filecontent) != 2: return
        except:
            return

        #store length of first word in n
        n = len(filecontent[0])
        #store length of second word in m
        m = len(filecontent[1])

        #store list of size n with each containing number of m zeros
        #base case: empty character will be initialise with 0
        memo = [[0 for i in range(m+1)] for i in range(n+1)]

        #Loops n time
        for N in range(1,n+1):
            #loop m time
            for M in range(1,m+1):
                # if second words is not equal to first words
                # get maximum of previous row or previous colummn optimal solution
                if filecontent[1][M-1] != filecontent[0][N-1]:
                    if memo[N - 1][M] >= memo[N][M - 1]:
                        memo[N][M] = memo[N - 1][M]
                    else:
                        memo[N][M] = memo[N][M - 1]
                else:
                    #otherwise add 1 with optimal solution, last row and last column
                    memo[N][M] = 1 + memo[N-1][M-1]

        #store a temporary string of reverse order of optimal solution
        string = ""
        # backtracking using bottom up approach
        while n > 0 and m > 0:
            #when first word is not equals to  second words and
            #memo of previous solution of second words is more than memo of previous solution of first word
            if filecontent[1][m-1] != filecontent[0][n-1] and memo[n-1][m] > memo[n][m-1]:
                n -= 1
            #when first word equals to second words
            # add string with firstword of current n value
            # backtracking by reducing n and m to go to next character
            elif filecontent[1][m-1] == filecontent[0][n-1]:
                string += filecontent[1][m - 1]
                n -= 1
                m -= 1
            #reduce m for first word equal to second word but
            #memo of previous solution of second words is lsessthan or equal memo of previous solution of first word
            else:
                m -= 1
        #store back string in reverse order which was part of backtracking approach
        self.message = ""
        for char in range(len(string)-1,-1,-1):
            self.message += string[char]

    def wordBreak(self,filename):
        """
        :param filename: name of a file
        :return: nothing, return statement is used to avoid crashing on file input.
        Time complexity: O(k*M*N*M), occurs when checking if each combination of substrings in string is in dictionary.
                        The time complexity get worse when all word in dictionary are having M character, so each substring of
                        input string,instance message is needed to compare all words in dictionary.
        Space complexity: O(k*M+N*M), occurs when list of dictionary is readed from file which would takes O(NM) and
                        adjency matrix is created to check if substring in input string is in dictionary which would takes O(kM)
                        therefore, space complexity would takes O(kM+NM) for adjency matrix and list of dictionary.
        where k is size of input string, N be the number of words in dictionary and
        M be the maximal size of the words in dictionary respectively.
        Pre-requisite: file must not be empty, each words in seperate line, dictionary file must exist.
        """
        #try to read dictionary file, ensure the file exist and length of dictionary should not be empty
        #when any of condition true, return to exit function
        try:
            with open(filename) as file:
                dict = []
                for line in file:
                    dict.append(line.strip())
                file.close()
        except:
            return
        #get instance message
        currentMessage = self.getMessage()
        #get longest words of dictionary and length of instance message
        M = self.maxDictLength(dict)
        k = len(currentMessage)
        #get adjency matrix which would hold 0 if substring of string exist in dictionary and
        #                                    1 if substring of string exist in dictionary
        possible = [[0 for i in range(k)] for i in range(M)]
        #loop through m times, for substring of instance string[j..j+m]
        for m in range(M):
            #define k as looping though k - m times
            k -= m
            # looping through j times for substrings of string instance message and check if
            # substrings of string[j..j+m] is in dictionary, if it is
            # adjency matrix, possible is marked 1 means, it exist
            for j in range(k):
                for words in dict:
                    if self.compareWordAtPosition(currentMessage,words,j,j+m+1):
                        possible[m][j] = 1
                        break
            k += m
        #reinitialise k with length of instance message
        k = len(currentMessage)
        #create a memo which store number of character that current index i can iterate for k character
        #values of memo only holds at most M, therefore, backtracking from memo only took atmost M times in k list item
        memo = [0 for i in range(k)]
        #looping from longest length of dictionary to 0
        for m in range(M-1,-1,-1):
            #looping for length of instance message to 0
            for j in range(k):
                #check if adjency matrix that defines that substring of string exist in dictionary
                # let flag be a constraint to check if substring can be added to memo, assuming longest words
                # is already allocated some space in array, therefore new substring need to consider the space it can take
                if possible[m][j] == 1:
                    flag = True
                    #looping through m times to check if any value after the index i..i+m is allocated already
                    for i in range(m+1):
                        #when length of current substring is less than current allocated value in memo, flag it and
                        #break because new substring is not suitable to be optimal solution
                        if m + 1 <= memo[j + i]:
                            flag = False
                            break
                    if flag:
                        #when all condition is fulfilled, loop through j..i+j to allocated the new substrings
                        for i in range(m+1):
                            memo[j + i] = m + 1
        #use flaging to check if last iteration is a words
        isLastAWord = False
        #get counter to allocate substring to new instance message
        counter = 0
        #reset instance message
        self.message = ""
        #while counter is less than length of memo
        #loop through the memo to append the character either in a loops or 1 at a time
        while counter < len(memo):
            #when character added is > 0, it indicate it is a string from dictionary
            if memo[counter] > 0:
                #flag as current word is word from dictionary
                isLastAWord = True
                # as long as counter is after first substring
                if counter > 0:
                    # add extra space
                    self.message += " "
                #add the substring of instance message that found to new instance message
                #values of memo only holds at most M, therefore, backtracking from memo only took atmost M times in k list item
                for j in range(memo[counter]):
                    self.message += currentMessage[counter+j]
                counter += memo[counter]
            else:
                #when last iteration is a word and counter is after first substring
                # add a space before adding words
                if isLastAWord and counter > 0:
                    isLastAWord = False
                    self.message += " "
                #add a character that not in dictionary into instance message
                self.message += currentMessage[counter]
                counter += 1

    def maxDictLength(self,dictionary):
        """
        :param dictionary: list of words in dictionary
        :return: length of longest words in dictionary
        Time complexity: O(n), n times is needed to check which words in dictionary is longest by thier length.
        Space complexity: O(1), only a byte of memory is needed to store number.
        where n is number of words in dictionary
        Pre-requisite: dictionary is list of strings and not empty
        """
        #let current be zero for empty string
        current = 0
        #loop through n iterations to check for longest words in dictionary
        for item in dictionary:
            if len(item) > current:
                current = len(item)
        return current

    def compareWordAtPosition(self,string,dictWords,startposition,endposition):
        """
        :param string: define input string or instance message
        :param dictWords: a words from dictionary
        :param startposition: start of substring in instance message
        :param endposition: end of substring in instance message
        :return:
        Time complexity: O(m), m time is needed to compare for size of dictionary words with substring in instance message
        Space complexity: O(1), comparison is done only without space is needed.
        where m be the maximal size of the words in the dictionary
        Pre-requisite: nothing
        """
        #check if slicing position if same as length of dictionary words
        # when not same, return false
        if endposition-startposition != len(dictWords):
            return False
        #looping from slicing position to end to check if the words is same as one in dictionary word
        else:
            #m variable store number of character in dictionary words
            m = 0
            for i in range(startposition,endposition):
                if string[i] != dictWords[m]:
                    return False
                m += 1
        #return true when character in words and dictionary words is same, and both words have same length
        return True

if __name__ == '__main__':
    newDecipher = Decipher()
    inputfile = "encrypted.txt"
    dictionary ="dictionary.txt"
    print('The name of the file, contains two encrypted texts : ' + inputfile)
    print('The name of the dictionary file : ' + dictionary)
    print('-' * 70)
    newDecipher.messageFind(inputfile)
    print('Deciphered message is '+ newDecipher.getMessage())
    newDecipher.wordBreak(dictionary)
    print('True message is ' + newDecipher.getMessage())
    print('-' * 70)
    print('Program end')
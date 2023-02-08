import spacy
import math
## 4-17~ loads up greetings and goodbyes txt file (our 'training set') into 2 seprate arrays
nlp = spacy.load("en_core_web_lg") #Our dictionary.
GreetingsSample = []
GoodbyeSample = []
FileIn = open("Greetings.txt")##First get all the common greetings and add them to an array.
LineGreet = FileIn.readlines()
for file in LineGreet:

    GreetingsSample.append(file.strip())
FileIn.close()
FileIn = open("Goodbyes.txt")#Then we get all the common goodbyes and add them to another array
LineGoodbye = FileIn.readlines()
for file in LineGoodbye:

    GoodbyeSample.append(file.strip())
FileIn.close()
global PrintAdminFlag
PrintAdminFlag = True
## print(GreetingsSample)
#Input: A string containing words
#Output a 'normalized' string
#Use case: This definition lowercases the players' input and removes punct for the increase accuracy in determining if the input is a greeting our not.=========
def Normalize(input):
    first = False
    input = str(input)
    input = input.lower()
    Input_token = nlp(input)
    input = ""
    for i in Input_token:##this loop removes the punct and turns the token back into a plain string
        if(not i.is_punct and (first)):
            input = input + " "+ i.text
        else:
            if(not i.is_punct and (not first)):
                input = i.text
                first = True
    print(input)
    return input
##Input: The sentence that a player has typed
#Output: a bool flag determining if the input is a greeting or not.
#Use Case: Greetings and goodbyes should be excluded in determine relevence. This definition checks to see if the input is closely similar to a line found in the Greetings or Goodbyes txt file.
def CheckGreetingorGoodbye(PlayerInput):
   ## print(GreetingsSample)
    PlayerInput = Normalize(PlayerInput)
    FoundSimilar = False
    PlayerToken = nlp(PlayerInput)
    print("Similarities between player input and dataset:")
    for i in GreetingsSample:
        CurrentGreetToken = nlp(i)
        if(PrintAdminFlag):
            print(f"{PlayerToken.text}<-->{CurrentGreetToken.text}:", PlayerToken.similarity(CurrentGreetToken))
        if(PlayerToken.similarity(CurrentGreetToken)>.85):
            print("Input is similar to greeting: "+ CurrentGreetToken.text)
            print("This is a greeting. Excluding message from relevance")
            FoundSimilar = True
            break
    if (FoundSimilar):
        return FoundSimilar
    for i in GoodbyeSample:
        CurrentGoodbyeToken = nlp(i)
        if(PrintAdminFlag):
            print(f"{PlayerToken.text}<-->{CurrentGoodbyeToken.text}:", PlayerToken.similarity(CurrentGoodbyeToken))
        if(PlayerToken.similarity(CurrentGoodbyeToken)>.85):
            print("Input is similar to goodbye: "+ CurrentGoodbyeToken.text)
            print("This is a goodbye. Excluding message from relevance.")
            FoundSimilar = True
            break
    return FoundSimilar
#Input: A string of topics
#Output: The amount of topics
#Use case: This code returns the amount of topics the user has entered. This is important in order to determine if something is NOT relevent. If a word is not relevent to any topic, it is not relevent.
def CountWords(words):
    count = len(words.split())
    return count
##future design is required. This should do something on Discord to let admins know something is going off the beaten path.
def ActionRequired(Topic):
    print("Hello Admin, some user is on-topic for one or more of the follow:" + Topic + "It is advise to take apprroiate action")
def TogglePrintFlag():
    global PrintAdminFlag
    if(PrintAdminFlag):
        PrintAdminFlag = False
        print("Similarities will no longer be printed to the terminal")
    else:
        PrintAdminFlag = True
        print("Similarities will now be printed to terminal")

def AdminTools():
    global PrintAdminFlag
    print("Hello Admin, please pick your selection:")
    print("To enable printing similarities to screen, enter 1")
    print("To change the category, enter 2")
    DecisionInt = input("Enter your number. All other entries will exit this prompt without change: ")
    if(DecisionInt == "1"):
        TogglePrintFlag()
    if(DecisionInt == "2"):
        print("WIP")





##Input: A single token
#Output: If the token is a noun/verb, return true. Else return false
#Use Case: Nouns are verbs are the only pos_ that are useful in determining relevant. Ex: The word 'and' should not be used in determine relevance.
def RemoveWord(SentToken):
   
    
    if(SentToken.pos_=="NOUN"):
       
        return True
    if(SentToken.pos_=="VERB"):
       
        return True
    

    return False
#Input: yes, the amount of relevent words, and no, the amount of nonrelevent words
#Output: Directly none, but it does modify the global variable trend.
#Use Case: If the ratio between on off topic and on topic is 3:1, the global variable, trend, gets +1. Else trend gets -1 (min 0). If trend is >=5, action should be employed.
def RatioChecker(yes,no):
   global trend
   if(yes!=0):
        div = math.gcd(no, yes)
        top = no/div
        bottom = yes/div
        if(top/bottom > 3):##GCD is used to determine ratio
            print("This message is off-topic")
            trend += 1
        else:
            print("This message is on topic")
            if(trend > 0):
                trend -= 1
   else:
       print("This message is definately off topic")
       trend += 1
   print("trend count: " + str(trend))
   if(trend>=5):
        ActionRequired(OurTopics)



#Input The topics that were decided by the admin, and oursentences, sent by the players.
#Output prints out of the similarity each word token is compared to each topic
#Use Case: The following def uses the following words:
# 1. Look at the lemmas of the nouns and verbs and tosses the rest out. The rest is not needed to determine relvence
# 2. These nouns/verbs gives 'Relevant' a +1 if it's similar to a topic by at least %50. A nouns/verb can relevent to many topics (aka, it's super relevant)
# 3. The only way a noun/verb can be 'NotRelevent' if it's not similar to ANY topic
# 4. 'Relevant' and 'NotRelevent' are passed to RatioChecker to see if NotRev/Rel is 3:1

def Relevence(OurSentences, OurTopics, length):
   
    Relevant = 0
    NotRelevant = 0
    RCount = 0
    Topic_Token = nlp(OurTopics) #tokenize both our strings
    Sentence_token = nlp(OurSentences)
    w=0
    for k in Sentence_token:
        TestText = ""
        for i in Topic_Token:
            
            if(RemoveWord(k)):
                ThisWord = k.lemma_
                This_Token = nlp(ThisWord)
                TestText = This_Token.text
                if(PrintAdminFlag):
                    print(f"{This_Token[0].text}<-->{i.text}:", This_Token[0].similarity(i))
                if(This_Token[0].similarity(i)>.50):
                    Relevant += 1
                    print(This_Token[0].text+" is relevant")
                else:
                    RCount += 1
                 ##   print(RCount)
                  ##  print(length)
                    

        if(RCount ==length):##If our words does not matches with any topic, it's not relevant.
            NotRelevant += 1
            print(TestText + " is not relevant")
        RCount = 0
    print("Relevant Count: " + str(Relevant) + "\nNot Relevent Count: "+ str(NotRelevant))
    RatioChecker(Relevant,NotRelevant)


global trend
trend = 0
lengthoffile = 0;
OurCategory = input("Hello Admin. Please enter the approved category (see txt files):")##grabs the approved topics from a txt file. Ideally, this txt file should be massive. The print from 81 can get huge, which is what we don't want for demo purposes.
FileIn = open(OurCategory+".txt")##The end product will have multiple trends and 'OurTopics' for multiple channels
OurTopics = FileIn.read()##The end product should allow an admin to add to these topics.

for line in FileIn:
    OurTopics = OurTopics + FileIn.read()#converts the contents of the file into one string
FileIn.close()
lengthoffile = CountWords(OurTopics)
OurTopics = OurTopics.replace("\n"," ") #For tokenization, we do not want indentation. (The txt file is indented to make it look nice)
print(OurTopics)
OurSentence = input("Please type sentences here (or -1 to exit, -2 for Admin Tools):")#This is to simulate people messaging on Discord.
while(OurSentence != "-1"):
    ChooseFlag = True
    if(OurSentence == "-2" and ChooseFlag):
        AdminTools()
        ChooseFlag = False
    if(ChooseFlag):
        if(OurSentence != -1 and (not CheckGreetingorGoodbye(OurSentence))):
            print(ChooseFlag)
            if(PrintAdminFlag):
                print("length:"+ str(lengthoffile))
            Relevence(OurSentence, OurTopics, lengthoffile)
            ChooseFlag = False
    OurSentence = input("Please type sentences here(or -1 to exit, or -2 for admin tools):")
print("Out of loop. Ending program.")

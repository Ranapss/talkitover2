#import files
from flask import Flask, render_template, request, make_response
from json import dumps
from datetime import datetime
import json
import time
#from textblob import TextBlob # was using this, but it doesn't seem to be working on Sanjay's machine
#import nltk
import random
import csv #check if this is still being used. i have a feeling we were going to use it but then decided against
app = Flask(__name__)
my_dict = {} # shoudl this be tidied up and deleted out?
sleep_per_word = 0.04 # I don't think this is being used yet, but could use it in the future
scores = [-0.5, 0, 0.3]
# the below encouragingNoises are things the bot might say to the user
encouragingNoises = ["I'm still listening, so feel free to say more.", "Go on talking, I'm still here.", \
"Keep talking, I'll be here for as long as you need me.", \
"I hear you. Keep going, I'm really happy for you to continue talking for as long as you need.", \
"Thanks for sharing this. Keep talking, I'm still here, and I'm still listening.", \
"I'm still here, so keep talking for as long as you need", "I'm still here, keep talking.", \
"Hmmm, thanks for sharing that. Keep talking, I'm still here", \
"Please keep on talking, I'm still here.", "Keep going, I'm still here", \
"Thanks for sharing. I'm still listening, so if you have more to say, please go on", \
"I hear you. Keep talking...", \
"Keep talking, I'm listening to you.", "Thanks for sharing, keep talking...", \
"I'm still listening, go on...", "I hear you, thank you for sharing, please keep talking", \
"Mhm, thanks for sharing this, please keep going", "Mhm, I hear you, go on talking",\
"I'm still here, feel free to continue talking as long as it's helping you", "Mhm, I hear you...",\
"Thank you for sharing. I'm still listening...", "I hear you. I'm still here...", "I hear you...",\
"Mhm, I hear you, thank you for sharing" ]


noOfEncouragingNoises = len(encouragingNoises)
section = 0
dataToStore = []
USER_CHARACTER_COUNT = 0
conversationId = str(datetime.now())
iWantToKillMyselfResponseAlreadyUsed = [conversationId,False]
imGoingToKillMyselfResponseAlreadyUsed = [conversationId,False]
iWantToDieResponseAlreadyUsed = [conversationId,False]
imFeelingSuicidalResponseAlreadyUsed = [conversationId,False]
#feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
suicidalThoughtsResponseAlreadyUsed = [conversationId,False]
iDontWantToLiveResponseAlreadyUsed = [conversationId,False]
shouldIKillMyselfResponseAlreadyUsed = [conversationId,False]
cryingResponseAlreadyUsed = [conversationId,False]
nothingToLiveForResponseAlreadyUsed = [conversationId,False]
singleWordDepressionResponseAlreadyUsed = [conversationId,False]
feelingDepressedResponseAlreadyUsed = [conversationId,False]
iHaveNoWayOutResponseAlreadyUsed = [conversationId,False]
hadEnoughOfLifeResponseAlreadyUsed = [conversationId,False]
nothingToLookForwardToResponseAlreadyUsed = [conversationId,False]
imUselessResponseAlreadyUsed = [conversationId,False]
imWorthlessResponseAlreadyUsed = [conversationId,False]
feelingLonelyResponseAlreadyUsed = [conversationId,False]
dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,False]
iHateHowILookResponseAlreadyUsed = [conversationId,False]
feelOverwhelmedResponseAlreadyUsed = [conversationId,False]
feelingAwfulResponseAlreadyUsed = [conversationId,False]
imAFailureResponseAlreadyUsed = [conversationId,False]
imALetdownResponseAlreadyUsed = [conversationId,False]
letMyselfDownResponseAlreadyUsed = [conversationId,False]
feelOutOfControlResponseAlreadyUsed = [conversationId,False]
feelLostResponseAlreadyUsed = [conversationId,False]
inABadPlaceResponseAlreadyUsed = [conversationId,False]
deserveResponseAlreadyUsed = [conversationId,False]
iHateHowIFeelResponseAlreadyUsed = [conversationId,False]
imSadResponseAlreadyUsed = [conversationId,False]
feelingLowDownTerribleResponseAlreadyUsed = [conversationId,False]
imUpsetResponseAlreadyUsed = [conversationId,False]
imAddictedResponseAlreadyUsed = [conversationId,False]
feelingRubbishResponseAlreadyUsed = [conversationId,False]
iHaveAnxietyResponseAlreadyUsed = [conversationId,False]
imAnxiousResponseAlreadyUsed = [conversationId,False]
imWorriedResponseAlreadyUsed = [conversationId,False]
iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,False]
initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
imNotHappyResponseAlreadyUsed = [conversationId,False]
iHateMyselfResponseAlreadyUsed = [conversationId,False]
difficultDayResponseAlreadyUsed = [conversationId,False]
familyProblemsResponseAlreadyUsed = [conversationId,False]
feelLostResponseAlreadyUsed = [conversationId,False]
doYouGiveAdviceResponseAlreadyUsed = [conversationId,False]


####### TODO TODO TODO ###################################
## Implement a separate css class for confidential text
## Maybe consider having a button which the user can press to say "you didn't understand me"
## Instead of the user's response being a dropdown, change it to a button so that it can be sized appropriately (i.e. not be tiny on a mobile screen)
## Correct the current bug: currently the system won't choose responses correctly if multiple users in parallel (or even in series)
## Do a refactor (maybe use more object oriented programming????)
## One thing to refactor: all the blahblahAlreadyUsed variables could be replaced with a dict?
## Currently have hardcoded "if section == 11" statements. replace these by having a variable for "numberOfInitialSections" = 10. Make sure it's global. If the user's first message is "hello", then increment the number of initial sections variable
## Stop button sometimes gets hit the moment it appears. Current fix is to add some wording; could consider something better?
## ADD IN WILDCARD BETWEEN "ITS NOT THAT" AND "STRING" WHERE APPLICABLE
## ADD IN SOMETHING FOR "YOU ARE NOT HELPING" OR "THIS IS NOT HELPING" OR "YOU ARE USELESS"
## Rules around selfharm / DSH / cutting -- this is still a gap
## Rules for relationships -- this comes up a lot, and I currently can't think of something good to say
## Rule for pandemic/corona/covid
## Longer term: would be great to be able to summarise back what the user has said (but this is hard!)
##########################################################



def initialiseResponseAlreadyUsedVariables():
    ## this function gets called *within* the app route, to make sure that the variables get initialised correctly
    ## note the structure of the variables: it includes the conversationId; this is to ensure that
    ## the app doesn't get confused when two users are using the bot concurrently (or, indeed, one after the other?)
    global conversationId
    print("This statement is in initialiseResponseAlreadyUsedVariables. conversationId = "+conversationId)
    iWantToKillMyselfResponseAlreadyUsed = [conversationId,False]
    imGoingToKillMyselfResponseAlreadyUsed = [conversationId,False]
    iWantToDieResponseAlreadyUsed = [conversationId,False]
    imFeelingSuicidalResponseAlreadyUsed = [conversationId,False]
    #feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
    suicidalThoughtsResponseAlreadyUsed = [conversationId,False]
    iDontWantToLiveResponseAlreadyUsed = [conversationId,False]
    shouldIKillMyselfResponseAlreadyUsed = [conversationId,False]
    cryingResponseAlreadyUsed = [conversationId,False]
    nothingToLiveForResponseAlreadyUsed = [conversationId,False]
    singleWordDepressionResponseAlreadyUsed = [conversationId,False]
    feelingDepressedResponseAlreadyUsed = [conversationId,False]
    iHaveNoWayOutResponseAlreadyUsed = [conversationId,False]
    hadEnoughOfLifeResponseAlreadyUsed = [conversationId,False]
    nothingToLookForwardToResponseAlreadyUsed = [conversationId,False]
    imUselessResponseAlreadyUsed = [conversationId,False]
    imWorthlessResponseAlreadyUsed = [conversationId,False]
    feelingLonelyResponseAlreadyUsed = [conversationId,False]
    dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,False]
    iHateHowILookResponseAlreadyUsed = [conversationId,False]
    feelOverwhelmedResponseAlreadyUsed = [conversationId,False]
    feelingAwfulResponseAlreadyUsed = [conversationId,False]
    imAFailureResponseAlreadyUsed = [conversationId,False]
    imALetdownResponseAlreadyUsed = [conversationId,False]
    letMyselfDownResponseAlreadyUsed = [conversationId,False]
    feelOutOfControlResponseAlreadyUsed = [conversationId,False]
    feelLostResponseAlreadyUsed = [conversationId,False]
    inABadPlaceResponseAlreadyUsed = [conversationId,False]
    deserveResponseAlreadyUsed = [conversationId,False]
    iHateHowIFeelResponseAlreadyUsed = [conversationId,False]
    imSadResponseAlreadyUsed = [conversationId,False]
    feelingLowDownTerribleResponseAlreadyUsed = [conversationId,False]
    imUpsetResponseAlreadyUsed = [conversationId,False]
    imAddictedResponseAlreadyUsed = [conversationId,False]
    feelingRubbishResponseAlreadyUsed = [conversationId,False]
    iHaveAnxietyResponseAlreadyUsed = [conversationId,False]
    imAnxiousResponseAlreadyUsed = [conversationId,False]
    imWorriedResponseAlreadyUsed = [conversationId,False]
    iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,False]
    initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
    second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
    imNotHappyResponseAlreadyUsed = [conversationId,False]
    iHateMyselfResponseAlreadyUsed = [conversationId,False]
    difficultDayResponseAlreadyUsed = [conversationId,False]
    familyProblemsResponseAlreadyUsed = [conversationId,False]
    feelLostResponseAlreadyUsed = [conversationId,False]
    doYouGiveAdviceResponseAlreadyUsed = [conversationId,False]


# returns the first index where an element occurs.
# not using this at time of writing; if we don't end up using this, could delete it out at next refactor
def bisect_left(a, x):

    hi = len(a)
    lo = 0
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] >= x: hi = mid
        else: lo+=1
    return lo

# get a response message from a yes, no answer
# currently not being used. could delete this???????
def get_yes_no(message, yes_message, no_message, not_understand_message, section):
    print("message ="+str(message))
    words = [i.lower() for i in message.split()]
    next_section = section
    print("this si the get_yes_no function")
    print(words, "sure" in words)
    if (("yes" in words) or ("yeah" in words) or ("yep" in words) or ("sure" in words)) and (("no" in words) or (" ".join(words[:2])=="not really")):
        response = not_understand_message[0]
        next_section += not_understand_message[1]
    elif ((("yes" not in words) and ("yeah" not in words))  and ("yep" not in words) and ("sure" not in words) and (" ".join(words[:2])!="not really") and ("no" not in words)):
        response = not_understand_message[0]
        next_section += not_understand_message[1]
    elif ("yes" in words) or ("yeah" in words) or ("yep" in words) or ("sure" in words):
        response = yes_message[0]
        next_section +=yes_message[1]
    elif ("no" in words) or " ".join(words[:2])=="not really":
        response = no_message[0]
        next_section += no_message[1]
    else:
        response="Error"
    return [response, next_section]

def write_data(anonymous, conversationId, message, response):
    ## stores the messages to file, if the user agrees
    ## need to adjust this -- currently this just stops recording abruptly at the moment the user says "confidential"...
    ## ... however should at least continue to the end of the button-clicking section and then
    ## ... stop recroding before the user says any free text of their own
    if anonymous=="true":
        message = message.replace(",", "¬")
        response = response.replace(",", "¬")

        with open('storedData.csv', 'a') as f:
            dataToStore = [str(conversationId), "User says:",str(message), "Chatbot says:",str(response)]
            f.write("\n" + str(dataToStore))
    return None

def next_user_input_one(buttonText):
    ## when we send certain strings of html to the client side, this function helps with that
    html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='"+buttonText+"'>"+buttonText+"</option> \
    </select>"
    return html_text

def next_user_input_two(buttonText1,buttonText2):
    ## when we send certain strings of html to the client side, this function helps with that
    html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='"+buttonText1+"'>"+buttonText1+"</option> \
    <option value='"+buttonText2+"'>"+buttonText2+"</option> \
    </select>"
    return html_text

def no_of_fragments_in_str_or_list(response):
    ## Sometimes the bot response is just one fragment; at other times one fragment will appear,...
    ## ... and then a typing ellipsis will appear for a moment, and then another fragment.
    ## This function counts the number of fragments
    noOfResponseFragments = 0
    if isinstance(response,list):
        noOfResponseFragments = len(response)
    elif isinstance(response,str):
        noOfResponseFragments = 1
    else:
        print("Error: expecting the response variable to be either a string or a list, otherwise don't know how to set the noOfResponseFragments variable")
    return noOfResponseFragments

def choose_bot_wordy_response(message):
    """
    In the free text section of the bot, this function chooses what the bot says.
    This function is called in the get_bot_response function.
    The function chooses by searching the user's message for a keyword, according to a priority ranking.
    There are specific bot responses to give for each keyword.
    If no keyword is found, a randomly generated encouraging phrase is chosen
    """

    ## KEYWORDS

    # iWantToKillMyself
    # iWantToDie
    # feelingSuicidal
    # feelingQuiteSuicidal
    # suicidalThoughts
    # crying
    # nothingToLiveFor
    # singleWordDepression
    # feelingDepressed
    # iHaveNoWayOut
    # hadEnoughOfLife
    # nothingToLookForwardTo
    # imUseless
    # imWorthless
    # feelingLonely
    # dontHaveAnyoneICanTalkTo
    # iHateHowILook
    # feelOverwhelmed
    # feelingAwful
    # letMyselfDown
    # feelOutOfControl
    # feelLost
    # inABadPlace
    # deserve
    # imSad
    # feelingLowDownTerrible
    # imUpset
    # imAddicted
    # feelingRubbish
    # iDontKnowWhatToSay
    # imNotHappy
    # iHateMyself
    # difficultDay
    # familyProblems
    # feelLost
    # doYouGiveAdvice



    global USER_CHARACTER_COUNT

    itsNotThatArray = ["it's not that", "its not that", "it's not tat", "its not tat",\
                        "i don't think", "i dont think", "i don't thnk", "i dont thnk",\
                        "i don't believe", "i dont believe", "i don't belive", "i dont belive",\
                        "i don't feel", "i dont feel",\
                        "i don't reckon", "i dont reckon",\
                        "i don't think that", "i dont think that", "i don't thnk that", "i dont thnk that",\
                        "i don't believe that", "i dont believe that", "i don't belive that", "i dont belive that",\
                        "i don't feel that", "i dont feel that",\
                        "i don't reckon that", "i dont reckon that"]
    # this section creates arrays of synonyms relating to things which a user might say. Typically each element
    # of the array is an "equivalence class", by which I mean that they are basically the same thing, but
    # might differ only in terms of anticipating typos, or perhaps including intensifiers (like "really")
    iWantToKillMyselfArray = ["i want to kill myself", "i want to kill my self", "i want to kill mysefl", "i want to kill my sefl", "i wanna kill myself", "i wanna kill my self", "i wanna kill mysefl", "i wanna kill my sefl",\
                            "i just want to kill myself", "i just want to kill my self", "i just want to kill mysefl", "i just want to kill my sefl", "i just wanna kill myself", "i just wanna kill my self", "i just wanna kill mysefl", "i just wanna kill my sefl",\
                            "i still just want to kill myself", "i still just want to kill my self", "i still just want to kill mysefl", "i still just want to kill my sefl", "i still just wanna kill myself", "i still just wanna kill my self", "i still just wanna kill mysefl", "i still just wanna kill my sefl",\
                            "i still want to kill myself", "i still want to kill my self", "i still want to kill mysefl", "i still want to kill my sefl", "i still wanna kill myself", "i still wanna kill my self", "i still wanna kill mysefl", "i still wanna kill my sefl",\
                            "i really want to kill myself", "i really want to kill my self", "i really want to kill mysefl", "i really want to kill my sefl", "i really wanna kill myself", "i really wanna kill my self", "i really wanna kill mysefl", "i really wanna kill my sefl",\
                            "i just really want to kill myself", "i just really want to kill my self", "i just really want to kill mysefl", "i just really want to kill my sefl", "i just really wanna kill myself", "i just really wanna kill my self", "i just really wanna kill mysefl", "i just really wanna kill my sefl",\
                            "i still just really want to kill myself", "i still just really want to kill my self", "i still just really want to kill mysefl", "i still just really want to kill my sefl", "i still just really wanna kill myself", "i still just really wanna kill my self", "i still just really wanna kill mysefl", "i still just really wanna kill my sefl",\
                            "i still really want to kill myself", "i still really want to kill my self", "i still really want to kill mysefl", "i still really want to kill my sefl", "i still really wanna kill myself", "i still really wanna kill my self", "i still really wanna kill mysefl", "i still really wanna kill my sefl",
                            "i want to take my life", "i wanna take my life", "i want to take my own life", "i wanna take my own life"]
    imGoingToKillMyselfArray = ["i am going to kill myself", "im going to kill myself", "i am going to kill my self", "im going to kill my self",
                                "i am oging to kill myself", "im oging to kill myself", "i am oging to kill my self", "im oging to kill my self",
                                "i will kill myself", "i will kill my self","ill kill myself", "ill kill my self"]
    #imPlanningToKillMyselfArray = ["im planning to kill myself", "i am planning to kill myself"]
    # have not built in anything for imPlanningToKillMyselfArray apart from the array itself. Maybe come back to this?
    iWantToDieArray = ["i want to die", "i wanna die", "i would like to die"]
    imFeelingSuicidalArray = ["i feel suic", "i'm feeling suic", "im feeling suic", "i just feel suic", "i'm just feeling suic", "im just feeling suic", "i'm suic", "im suic", "i am suic",\
                            "i feel sucid", "i'm feeling sucid", "im feeling sucid", "i just feel sucid", "i'm just feeling sucid", "im just feeling sucid", "i'm sucid", "im sucid", "i am sucid",\
                            "i still feel suic", "i'm still feeling suic", "im still feeling suic", "i still just feel suic", "i'm still just feeling suic", "im still just feeling suic", "i'm still suic", "im still suic",\
                            "i still feel sucid", "i'm still feeling sucid", "im still feeling sucid", "i still just feel sucid", "i'm still just feeling sucid", "im still just feeling sucid", "i'm still sucid", "im still sucid",
                            "im starting to feel suic", "i am starting to feel suic", "i have started to feel suic",
                            "im starting to feel sucid", "i am starting to feel sucid", "i have started to feel sucid",
                            "i am feeling suic", "i am feeling sucid"]
    imFeelingQuiteSuicidalArray = ["i feel quite suic", "i'm feeling quite suic", "im feeling quite suic", "i just feel quite suic", "i'm just feeling quite suic", "im just feeling quite suic",\
                                   "i feel quite sucid", "i'm feeling quite sucid", "im feeling quite sucid", "i just feel quite sucid", "i'm just feeling quite sucid", "im just feeling quite sucid",\
                                   "i still feel quite suic", "i'm still feeling quite suic", "im still feeling quite suic", "i still just feel quite suic", "i'm still just feeling quite suic", "im still just feeling quite suic",\
                                    "i still feel quite sucid", "i'm still feeling quite sucid", "im still feeling quite sucid", "i still just feel quite sucid", "i'm still just feeling quite sucid", "im still just feeling quite sucid"]
    #imThinkingAboutKillingMyselfArray = ["im thinking about killing myself", "i am thinking about killing myself"]
    # have not built in anything for imThinkingAboutKillingMyselfArray apart from the array itself. Maybe come back to this?
    iveBeenFeelingSuicidalArray = ["i've been feeling suic", "ive been feeling suic", "i've just been feeling suic", "ive just been feeling suic",\
                            "i've been feeling sucid", "ive been feeling sucid", "i've just been feeling sucid", "ive just been feeling sucid",]
    suicidalThoughtsArray = ["i have suicidal thoughts", "i still have suicidal thoughts", "i have been having suicidal thoughts"]
    iDontWantToLiveArray = ["i dont want to live", "i no longer want to live", "i dont wanna live", "i have no desire to live", "i no longer desire to live",
                            "i dont want to be alive", "i no longer want to be alive", "i dont wanna be alive", "i have no desire to be alive", "i no longer desire to be alive",
                            "i dont want to remain alive", "i no longer want to remain alive", "i dont wanna remain alive", "i have no desire to remain alive", "i no longer desire to remain alive",
                            "i dont want to stay alive", "i no longer want to stay alive", "i dont wanna stay alive", "i have no desire to stay alive", "i no longer desire to stay alive",
                            "i hate my life", "i hate being alive", "i hate the fact that im alive", "i hate living", "i hate the fact that i'm living"]
    shouldIKillMyselfArray = ["should i kill myself", "should i commit suicide", "should i end my life", "should i end it all"]
    imCryingArray = ["i can't stop crying","i cant stop crying", "makes me want to cry", "makes me wanna cry", "i'm crying", "im crying", "i've been crying", "ive been crying", "making me want to cry", "making me wanna cry", "i cry myself"]
    ## Note: imCryingArray doesn't contain the string "i cry" because the test involves removing the space characters,
    ## so a message containing something like "mimicry" would trigger the "i cry" response
    nothingToLiveForArray = ["i have nothing to live for", "i've nothing to live for", "i have nothing left to live for", "i've nothing left to live for", "i have no reason to live", "theres no point in me living",\
                            "i have nothing to be alive for", "i've nothing to be alive for", "i have nothing left to be alive for", "i've nothing left to be alive for", "i have no reason to be alive", "theres no point in me being alive",  "theres no point in my being alive",
                            "i have nothing to stay alive for", "i've nothing to stay alive for", "i have nothing left to stay alive for", "i've nothing left to stay alive for", "i have no reason to stay alive", "theres no point in me staying alive", "theres no point in my staying alive",
                            "i have nothing to remain alive for", "i've nothing to remain alive for", "i have nothing left to remain alive for", "i've nothing left to remain alive for", "i have no reason to remain alive", "theres no point in me remaining alive", "theres no point in my remaining alive"]
    iHateMyselfArray = [" hate myself", " hate my self", " hate my sefl", " hate mysefl",]
    singleWordDepressionMessageArray = ["depression", "depressed", "depresssion", "depresssed", "dperessed", "dperession"  ]
    feelingDepressedArray = ["i feel depressed", "i just feel depressed", "i feeel depressed", "i just feeel depressed", "im feeling depressed", "i'm feeling depressed", "im just feeling depressed", "i'm just feeling depressed", "i feel very depressed", "i feel so depressed", "i am feeling depressed", "i'm feeling really depressed", "i'm feeling so depressed", "im feeling really depressed", "im feeling so depressed",\
                            "i'm depressed", "im depressed", "i am depressed", "i'm so depressed", "im so depressed", "i am so depressed", "i'm really depressed", "im really depressed", "i am really depressed",\
                            "im more depressed than ever", "i'm more depressed than ever" ]
    iHaveNoWayOutArray = ["i have no way out", "i haven't got any way out", "ive got no way out", "ive no got any way out", "i don't feel i have any way out", "i dont feel i have any way out", "i don't feel i have got any way out", "i dont feel i have got any way out", "i don't have any way out", "i dont have any way out"]
    hadEnoughOfLifeArray = ["i've had enough of life", "ive had enough of life", "i have had enough of life"]
    nothingToLookForwardToArray = ["i have nothing to look forward to", "i don't have anything to look forward to", "i've got nothing to look forward to", \
                                "i literally have nothing to look forward to", "i literally don't have anything to look forward to", "i have literally nothing to look forward to", "i've literally got nothing to look forward to"\
                                "i just have nothing to look forward to", "i just don't have anything to look forward to", "i've just got nothing to look forward to",\
                                 "i've literally just got nothing to look forward to"]
    imUselessArray = ["im useless", "i'm useless", "im uselses", "i'm uselses","im usless", "i'm usless",\
                    "im so useless", "i'm so useless", "im so uselses", "i'm so uselses","im usless", "i'm usless",\
                    "im really useless", "i'm really useless", "im really uselses", "i'm really uselses","im usless", "i'm usless",\
                    "im totally useless", "i'm totally useless", "im totally uselses", "i'm totally uselses","im usless", "i'm usless",\
                    "im utterly useless", "i'm utterly useless", "im utterly uselses", "i'm utterly uselses", "im usless", "i'm usless",\
                    "im just useless", "i'm just useless", "im just uselses", "i'm just uselses","im just usless", "i'm just usless",\
                    "im just so useless", "i'm just so useless", "im just so uselses", "i'm just so uselses","im just usless", "i'm just usless",\
                    "im just really useless", "i'm just really useless", "im just really uselses", "i'm just really uselses","im just usless", "i'm just usless",\
                    "im just totally useless", "i'm just totally useless", "im just totally uselses", "i'm just totally uselses","im just usless", "i'm just usless",\
                    "im just utterly useless", "i'm just utterly useless", "im just utterly uselses", "i'm just utterly uselses", "im just usless", "i'm just usless"]
    imWorthlessArray = ["im worthless", "i'm worthless", "im worthlses", "i'm worthlses",\
                    "im so worthless", "i'm so worthless", "im so worthlses", "i'm so worthlses",\
                    "im really worthless", "i'm really worthless", "im really worthlses", "i'm really worthlses",\
                    "im totally worthless", "i'm totally worthless", "im totally worthlses", "i'm totally worthlses",\
                    "im utterly worthless", "i'm utterly worthless", "im utterly worthlses", "i'm utterly worthlses",\
                    "im just worthless", "i'm just worthless", "im just worthlses", "i'm just worthlses",\
                    "im just so worthless", "i'm just so worthless", "im just so worthlses", "i'm just so worthlses",\
                    "im just really worthless", "i'm just really worthless", "im just really worthlses", "i'm just really worthlses",\
                    "im just totally worthless", "i'm just totally worthless", "im just totally worthlses", "i'm just totally worthlses",\
                    "im just utterly worthless", "i'm just utterly worthless", "im just utterly worthlses", "i'm just utterly worthlses"]
    feelingLonelyArray = ["i feel lonely", "im feeling lonely", "i am feeling lonely","making me feel lonely", "making me lonely","makes me feel lonely", "makes me lonely",
                        "i feel alone", "im feeling alone", "i am feeling alone", "making me feel alone", "making me alone","makes me feel alone", "makes me alone",
                        "i feel sad and lonely", "im feeling sad and lonely", "i am feeling sad and lonely","making me feel sad and lonely", "making me sad and lonely", "makes me feel sad and lonely", "makes me sad and lonely",
                        "i feel low and lonely", "im feeling low and lonely", "i am feeling low and lonely", "making me feel low and lonely", "making me low and lonely", "makes me feel low and lonely", "makes me low and lonely",
                        "i feel sad and alone", "im feeling sad and alone", "i am feeling sad and alone", "making me feel sad and alone", "making me sad and alone", "makes me feel sad and alone", "makes me sad and alone",
                        "i feel low and alone", "im feeling low and alone", "i am feeling low and alone", "making me feel low and alone", "making me low and alone", "makes me feel low and alone", "makes me low and alone",
                        "i feel isolated", "im feeling isolated", "i am feeling isolated", "making me feel isolated", "making me isolated", "makes me feel isolated", "makes me isolated",
                        "i feel sad and isolated", "im feeling sad and isolated", "i am feeling sad and isolated", "making me feel sad and isolated", "making me sad and isolated", "makes me feel sad and isolated", "makes me sad and isolated",
                            "im a lonely person", "i am a lonely person", "im a sad lonely person", "i am a sad lonely person",
                        "i am lonely", "im lonely", "i am lonely","making me lonely", "making me lonely","makes me lonely", "makes me lonely",
                        "im alone", "i am alone", "making me alone", "making me alone","makes me alone", "makes me alone",
                        "im sad and lonely", "i am sad and lonely","making me sad and lonely", "making me sad and lonely", "makes me sad and lonely", "makes me sad and lonely",
                        "im low and lonely", "i am low and lonely", "making me low and lonely", "making me low and lonely", "makes me low and lonely", "makes me low and lonely",
                        "im sad and alone", "i am sad and alone", "making me sad and alone", "making me sad and alone", "makes me sad and alone", "makes me sad and alone",
                        "im low and alone", "i am low and alone", "making me low and alone", "making me low and alone", "makes me low and alone", "makes me low and alone",
                        "im isolated", "i am isolated", "making me isolated", "making me isolated", "makes me isolated", "makes me isolated",
                        "im sad and isolated", "i am sad and isolated", "making me sad and isolated", "making me sad and isolated", "makes me sad and isolated", "makes me sad and isolated"]
    dontHaveAnyoneICanTalkToArray = ["don't have anyone i can talk to", "dont have anyone i can talk to","don't have anyone i can talk with", "dont have anyone i can talk with",
                                    "i have no one to talk to", "i have nobody to talk to", "i have no one to talk with", "i have nobody to talk with",
                                    "i've no one to talk to", "i've nobody to talk to", "i've no one to talk with", "i've nobody to talk with",
                                    "ive no one to talk to", "ive nobody to talk to", "ive no one to talk with", "ive nobody to talk with", ]
    iHateHowILookArray = ["i hate how i look", "i hate my looks", "i hate my appearance", "i hate the way i look",\
                        "i just hate how i look", "i just hate my looks", "i just hate my appearance", "i just hate the way i look",\
                        "i really hate how i look", "i really hate my looks", "i really hate my appearance", "i really hate the way i look",\
                        "i really just hate how i look", "i really just hate my looks", "i really just hate my appearance", "i really just hate the way i look"]
    feelOverwhelmedArray = ["i feel overwhelmed", "im feeling overwhelmed", "i'm feeling overwhelmed", \
                            "i feel so overwhelmed", "im feeling so overwhelmed", "i'm feeling so overwhelmed",\
                            "i feel really overwhelmed", "im feeling really overwhelmed", "i'm feeling really overwhelmed", \
                            "i feel totally overwhelmed", "im feeling totally overwhelmed", "i'm feeling totally overwhelmed",\
                            "i feel utterly overwhelmed", "im feeling utterly overwhelmed", "i'm feeling utterly overwhelmed",\
                            "i just feel overwhelmed", "im just feeling overwhelmed", "i'm just feeling overwhelmed", \
                            "i just feel so overwhelmed", "im just feeling so overwhelmed", "i'm just feeling so overwhelmed",\
                            "i just feel really overwhelmed", "im just feeling really overwhelmed", "i'm just feeling really overwhelmed", \
                            "i just feel totally overwhelmed", "im just feeling totally overwhelmed", "i'm just feeling totally overwhelmed",\
                            "i just feel utterly overwhelmed", "im just feeling utterly overwhelmed", "i'm just feeling utterly overwhelmed",
                            "i am overwhelmed", "im overwhelmed"]
    feelingAwfulArray = ["i feel awful", "i'm feeling awful", "im feeling awful",\
                        "i feel so awful", "i'm feeling so awful", "im feeling so awful",\
                        "i feel really awful", "i'm feeling really awful", "im feeling really awful",\
                        "i just feel awful", "i'm just feeling awful", "im just feeling awful",\
                        "i just feel so awful", "i'm just feeling so awful", "im just feeling so awful",\
                        "i just feel really awful", "i'm just feeling really awful", "im just feeling really awful"]
    imAFailureArray = ["im a failure", "i am a failure", "im a total failure", "i am a total failure", "im a total utter failure", "i am a total utter failure", "im an utter failure", "i am an utter failure",
                        "im just a failure", "i am just a failure", "im just a total failure", "i am just a total failure", "im just a total utter failure", "i am just a total utter failure", "im an utter failure", "i am an utter failure",
                        "im just a failure", "i really am just a failure", "im just a total failure", "i really am just a total failure", "im just a total utter failure", "i really am just a total utter failure", "im an utter failure", "i really am an utter failure",
                        "im a failure", "i really am a failure", "im a total failure", "i really am a total failure", "im a total utter failure", "i really am a total utter failure", "im an utter failure", "i really am an utter failure",
                        "im such a failure", "i am such a failure", "im such a total failure", "i am such a total failure", "im such a total utter failure", "i am such a total utter failure", "im such an utter failure", "i am such an utter failure",
                        "i feel like a failure", "i feel a failure", "i feel myself to be a failure",
                        "i feel like such a failure", "i feel such a failure", "i feel myself to be such a failure"]
    imALetdownArray = ["im a letdown", "i am a letdown", "im a total letdown", "i am a total letdown", "im a total utter letdown", "i am a total utter letdown", "im an utter letdown", "i am an utter letdown",
                        "im just a letdown", "i am just a letdown", "im just a total letdown", "i am just a total letdown", "im just a total utter letdown", "i am just a total utter letdown", "im an utter letdown", "i am an utter letdown",
                        "im just a letdown", "i really am just a letdown", "im just a total letdown", "i really am just a total letdown", "im just a total utter letdown", "i really am just a total utter letdown", "im an utter letdown", "i really am an utter letdown",
                        "im a letdown", "i really am a letdown", "im a total letdown", "i really am a total letdown", "im a total utter letdown", "i really am a total utter letdown", "im an utter letdown", "i really am an utter letdown",
                      "im a let down", "i am a let down", "im a total let down", "i am a total let down", "im a total utter let down", "i am a total utter let down", "im an utter let down", "i am an utter let down",
                        "im just a let down", "i am just a let down", "im just a total let down", "i am just a total let down", "im just a total utter let down", "i am just a total utter let down", "im an utter let down", "i am an utter let down",
                        "im just a let down", "i really am just a let down", "im just a total let down", "i really am just a total let down", "im just a total utter let down", "i really am just a total utter let down", "im an utter let down", "i really am an utter let down",
                        "im a let down", "i really am a let down", "im a total let down", "i really am a total let down", "im a total utter let down", "i really am a total utter let down", "im an utter let down", "i really am an utter let down",
                        "im such a letdown", "i am such a letdown", "im such a total letdown", "i am such a total letdown", "im such a total utter letdown", "i am such a total utter letdown", "im such an utter letdown", "i am such an utter letdown",
                        "i feel like a letdown", "i feel a letdown", "i feel myself to be a letdown",
                        "i feel like such a letdown", "i feel such a letdown", "i feel myself to be such a letdown"]
    letMyselfDownArray = ["let myself down", "let my self down", "let mysefl down", "let my sefl down"]
    feelOutOfControlArray = ["i feel out of control", "i'm feeling out of control", "im feeling out of control",\
                            "i feel so out of control", "i'm feeling so out of control", "im feeling so out of control",\
                            "i feel really out of control", "i'm feeling really out of control", "im feeling really out of control",\
                            "i feel totally out of control", "i'm feeling totally out of control", "im feeling totally out of control",\
                            "i just feel out of control", "i'm just feeling out of control", "im just feeling out of control",\
                            "i just feel so out of control", "i'm just feeling so out of control", "im just feeling so out of control",\
                            "i just feel really out of control", "i'm just feeling really out of control", "im just feeling really out of control",\
                            "i just feel totally out of control", "i'm just feeling totally out of control", "im just feeling totally out of control"]
    feelLostArray = ["i feel lost", "i'm feeling lost", "im feeling lost", \
                    "i feel so lost", "i'm feeling so lost", "im feeling so lost",\
                    "i feel totally lost", "i'm feeling totally lost", "im feeling totally lost",\
                    "i feel utterly lost", "i'm feeling utterly lost", "im feeling utterly lost",\
                    "i feel really lost", "i'm feeling really lost", "im feeling really lost",\
                    "i feel very lost", "i'm feeling very lost", "im feeling very lost",\
                    "i just feel lost", "i'm just feeling lost", "im just feeling lost", \
                    "i just feel so lost", "i'm just feeling so lost", "im just feeling so lost",\
                    "i just feel totally lost", "i'm just feeling totally lost", "im just feeling totally lost",\
                    "i just feel utterly lost", "i'm just feeling utterly lost", "im just feeling utterly lost",\
                    "i just feel really lost", "i'm just feeling really lost", "im just feeling really lost",\
                    "i just feel very lost", "i'm just feeling very lost", "im just feeling very lost"]
    inABadPlaceArray = ["i am in a bad place", "i'm in a bad place", "im in a bad place",\
                        "i am in such a bad place", "i'm in such a bad place", "im in such a bad place",\
                        "i am at a bad place", "i'm at a bad place", "im at a bad place",\
                        "i am at such a bad place", "i'm at such a bad place", "im at such a bad place"]
    feelingLowDownTerribleArray = ["i feel low", "i'm feeling low", "im feeling low", " i feel down", "i'm feeling down", "im feeling down", "i feel terrible", "i'm feeling terrible", "im feeling terrible", "i feel horrible", "i'm feeling horrible", "im feeling horrible",\
                                "i feel so low", "i'm feeling so low", "im feeling so low", "i feel so down", "i'm feeling so down", "im feeling so down", "i feel so terrible", "i'm feeling so terrible","im feeling so terrible", "i feel so horrible", "i'm feeling so horrible", "im feeling so horrible",\
                                "i feel really low", "i'm feeling really low", "im feeling really low", "i feel really down", "i'm feeling really down", "im feeling really down", "i feel really terrible", "i'm feeling really terrible", "im feeling really terrible", "i feel really horrible", "i'm feeling really horrible",\
                                "i feel totally low", "i'm feeling totally low", "im feeling totally low", "i feel totally down", "i'm feeling totally down", "im feeling totally down", "i feel totally terrible", "i'm feeling totally terrible", "im feeling totally terrible", "i feel totally horrible", "i'm feeling totally horrible", "im feeling totally horrible",\
                                "i feel utterly low", "i'm feeling utterly low", "im feeling utterly low", "i feel utterly down", "i'm feeling utterly down", "im feeling utterly down", "i feel utterly terrible", "i'm feeling utterly terrible", "im feeling utterly terrible", "i feel utterly horrible", "i'm feeling utterly horrible", "im feeling utterly horrible",\
                                "i just feel low", "i'm just feeling low", "im just feeling low", " i just feel down", "i'm just feeling down", "im just feeling down", "i just feel terrible", "i'm just feeling terrible", "im just feeling terrible", "i just feel horrible", "i'm just feeling horrible", "im just feeling horrible",\
                                "i just feel so low", "i'm just feeling so low", "im just feeling so low", "i just feel so down", "i'm just feeling so down", "im just feeling so down", "i just feel so terrible", "i'm just feeling so terrible","im just feeling so terrible", "i just feel so horrible", "i'm just feeling so horrible", "im just feeling so horrible",\
                                "i just feel really low", "i'm just feeling really low", "im just feeling really low", "i just feel really down", "i'm just feeling really down", "im just feeling really down", "i just feel really terrible", "i'm just feeling really terrible", "im just feeling really terrible", "i just feel really horrible", "i'm just feeling really horrible",\
                                "i just feel totally low", "i'm just feeling totally low", "im just feeling totally low", "i just feel totally down", "i'm just feeling totally down", "im just feeling totally down", "i just feel totally terrible", "i'm just feeling totally terrible", "im just feeling totally terrible", "i just feel totally horrible", "i'm just feeling totally horrible", "im just feeling totally horrible",\
                                "i just feel utterly low", "i'm just feeling utterly low", "im just feeling utterly low", "i just feel utterly down", "i'm just feeling utterly down", "im just feeling utterly down", "i just feel utterly terrible", "i'm just feeling utterly terrible", "im just feeling utterly terrible", "i just feel utterly horrible", "i'm just feeling utterly horrible", "im just feeling utterly horrible"]
    iHateHowIFeelArray = ["i hate how i feel","i hate how im feeling", "i hate my feelings"]
    imSadArray = ["i am sad", "i'm sad", "im sad",
                "i am feeling sad", "i'm feeling sad", "im feeling sad"]
    imUpsetArray = ["im upset", "i'm upset", "im feeling upset", "i'm feeling upset", "i feel upset", "i feel upset",\
                    "im so upset", "i'm so upset", "im feeling so upset", "i'm feeling so upset", "i feel so upset", "i feel so upset",\
                    "im really upset", "i'm really upset", "im feeling really upset", "i'm feeling really upset", "i feel really upset", "i feel really upset"]
    imAddictedArray = ["im addicted", "i'm addicted"]
    feelingRubbishArray = ["im feeling rubbish", "i'm feeling rubbish", "i feel rubbish", "i feel rubbish",\
                    "im feeling so rubbish", "i'm feeling so rubbish", "i feel so rubbish", "i feel so rubbish",\
                    "im feeling really rubbish", "i'm feeling really rubbish", "i feel really rubbish", "i feel really rubbish",\
                    "im just feeling rubbish", "i'm just feeling rubbish", "i just feel rubbish", "i just feel rubbish",\
                    "im just feeling so rubbish", "i'm just feeling so rubbish", "i just feel so rubbish", "i just feel so rubbish",\
                    "im just feeling really rubbish", "i'm just feeling really rubbish", "i just feel really rubbish", "i just feel really rubbish"]
    imAnxiousArray = ["im anxious", "i am anxious", "im feeling anxious", "i am feeling anxious", "i feel anxious"]
    iHaveAnxietyArray = ["i have anxiety", "i suffer from anxiety"]
    imWorriedArray = ["im worried", "i am worried", "i have worries", "making me worried", "makes me worried", "leaves me feeling worried", " i have so much to worry "]
    imNotHappyArray = ["im not happy", "i'm not happy", "im just not happy", "i'm just not happy", "im really not happy", "i'm really not happy"]
    difficultDayArray = ["its been a tough day", "it's been a tough day", "i've had a tough day", "ive had a tough day", \
                        "its been a difficult day", "it's been a difficult day", "i've had a difficult day", "ive had a difficult day"]
    familyProblemsArray = ["i have family problems", "i'm having family problems", "im having family problems", "ive got family problems", \
                            "i have problems with my family", "i'm having problems with my family", "im having problems with my family", "ive got problems with my family",
                            "i have family troubles", "i'm having family troubles", "im having family troubles", "ive got family troubles", \
                            "i have troubles with my family", "i'm having troubles with my family", "im having troubles with my family", "ive got troubles with my family",
                            "i have family difficulties", "i'm having family difficulties", "im having family difficulties", "ive got family difficulties", "ive got difficulties with my family", \
                            "i have difficulties with my family", "i'm having difficulties with my family", "im having difficulties with my family", "ive got difficulties with my family", \
                            "i have family worries", "i'm having family worries", "im having family worries", "ive got family worries", "ive got worries with my family", \
                            "i have worries with my family", "i'm having worries with my family", "im having worries with my family", "ive got worries with my family"]
    iDontKnowWhatToDoArray = ["i dont know what to do", "i dunno what to do", "i have no idea what to do",
                            "ive no idea what to do", "i hvaent a clue what to do", "i havent a clue what to do",
                            "i havent any idea what to do", "i dont have any idea what to do",
                            "im not sure what to do", "im not all that sure what to do", "i am not sure what to do", "im not at all sure what to do",
                            "what do you think i should do", "what do you think i shuld do", "what do u think i should do", "wat do you think i should do",
                            "what should i do", "what can i do", "what do i do"]
    iDontKnowWhatToSayArray = ["i dont know what to say", "i don't know what to say", "i dont know what else to say", "i don't know what else to say", "i dont know what more to say", "i don't know what more to say",
                                "i dont know what to tell you", "i don't know what to tell you", "i dont know what else to tell you", "i don't know what else to tell you", "i dont know what more to tell you", "i don't know what more to tell you",
                                "dont know what to say", "don't know what to say", "dont know what else to say", "don't know what else to say", "dont know what more to say", "don't know what more to say",
                                "dont know what to tell you", "don't know what to tell you", "dont know what else to tell you", "don't know what else to tell you", "dont know what more to tell you", "don't know what more to tell you",
                                "i dont know what to say now", "i don't know what to say now", "i dont know what else to say now", "i don't know what else to say now", "i dont know what more to say now", "i don't know what more to say now",
                                "dont know what to say now", "don't know what to say now", "dont know what else to say now", "don't know what else to say now", "dont know what more to say now", "don't know what more to say now",
                                "dunno what to say", "dunno what else to say", "dunno what more to say",
                                "i dont really know what to say", "i don't really know what to say", "i dont really know what else to say", "i don't really know what else to say", "i dont really know what more to say", "i don't really know what more to say",
                                "i dont really know what to tell you", "i don't really know what to tell you", "i dont really know what else to tell you", "i don't really know what else to tell you", "i dont really know what more to tell you", "i don't really know what more to tell you",
                                "dont really know what to say", "don't really know what to say", "dont really know what else to say", "don't really know what else to say", "dont really know what more to say", "don't really know what more to say",
                                "dont really know what to tell you", "don't really know what to tell you", "dont really know what else to tell you", "don't really know what else to tell you", "dont really know what more to tell you", "don't really know what more to tell you",
                                "i dont really know what to say now", "i don't really know what to say now", "i dont really know what else to say now", "i don't really know what else to say now", "i dont really know what more to say now", "i don't really know what more to say now",
                                "dont really know what to say now", "don't really know what to say now", "dont really know what else to say now", "don't really know what else to say now", "dont really know what more to say now", "don't really know what more to say now"]
    helloArray = ["hello", "hi", "hey","hello!", "hi!", "hey!", "hello?", "hi?", "hey?"]
    doYouGiveAdviceArray = ["do you give advice", "do you provide advice","do you offer advice"
                            "do you give any advice", "do you provide any advice","do you offer any advice",
                            "do you even give advice", "do you even provide advice", "do you even offer advice",
                            "do you even give any advice", "do you even provide any advice",  "do you even offer any advice",
                            "can you give me advice", "can you provide me advice", "can you offer me advice",
                            "can you give me any advice", "can you provide me any advice", "can you offer me any advice",
                            "can you give me some advice", "can you provide me some advice", "can you offer me some advice",
                            "have you any advice", "have you some advice", "have you advice"
                            "give me advice", "i need advice",
                            "dont you give advice", "you dont give advice",
                            "will you give me advice", "will you give advice"]
    stopSynonymsArray = ["that's it", "thats it", "finish", "end", "nothing more to say", "no more to say", "bot stop", "bye","goodbye",\
                        "done", "i'm done", "im done", "i think im done", "im done speaking", "i think im done speaking",
                        "i have nothing more to say", "i have nothing else to say", "ive got nothing more to say", "ive got nothing else to say",
                        "i think i have nothing more to say", "i think i have nothing else to say", "i think ive got nothing more to say", "i think ive got nothing else to say",
                        "i dont want to talk any more" ]



    # these variables are to keep track of whether a response has already been given (to avoid repeating it).
    # Just asserting here that they are global
    global iWantToKillMyselfResponseAlreadyUsed
    global imGoingToKillMyselfResponseAlreadyUsed
    global iWantToDieResponseAlreadyUsed
    global imFeelingSuicidalResponseAlreadyUsed
    #global feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
    global suicidalThoughtsResponseAlreadyUsed
    global iDontWantToLiveResponseAlreadyUsed
    global shouldIKillMyselfResponseAlreadyUsed
    global cryingResponseAlreadyUsed
    global nothingToLiveForResponseAlreadyUsed
    global singleWordDepressionResponseAlreadyUsed
    global feelingDepressedResponseAlreadyUsed
    global iHaveNoWayOutResponseAlreadyUsed
    global hadEnoughOfLifeResponseAlreadyUsed
    global nothingToLookForwardToResponseAlreadyUsed
    global imUselessResponseAlreadyUsed
    global imWorthlessResponseAlreadyUsed
    global feelingLonelyResponseAlreadyUsed
    global dontHaveAnyoneICanTalkToResponseAlreadyUsed
    global iHateHowILookResponseAlreadyUsed
    global feelOverwhelmedResponseAlreadyUsed
    global feelingAwfulResponseAlreadyUsed
    global imAFailureResponseAlreadyUsed
    global imALetdownResponseAlreadyUsed
    global letMyselfDownResponseAlreadyUsed
    global feelOutOfControlResponseAlreadyUsed
    global feelLostResponseAlreadyUsed
    global inABadPlaceResponseAlreadyUsed
    global deserveResponseAlreadyUsed
    global iHateHowIFeelResponseAlreadyUsed
    global imSadResponseAlreadyUsed
    global feelingLowDownTerribleResponseAlreadyUsed
    global imUpsetResponseAlreadyUsed
    global imAddictedResponseAlreadyUsed
    global feelingRubbishResponseAlreadyUsed
    global iHaveAnxietyResponseAlreadyUsed
    global imAnxiousResponseAlreadyUsed
    global imWorriedResponseAlreadyUsed
    global iDontKnowWhatToDoResponseAlreadyUsed
    global initial_iDontKnowWhatToSayResponseAlreadyUsed
    global second_iDontKnowWhatToSayResponseAlreadyUsed
    global imNotHappyResponseAlreadyUsed
    global iHateMyselfResponseAlreadyUsed
    global difficultDayResponseAlreadyUsed
    global familyProblemsResponseAlreadyUsed
    global feelLostResponseAlreadyUsed
    global doYouGiveAdviceResponseAlreadyUsed


# declaring some variables which track whether a message says certain things
    msgSaysIWantToKillMyself = False
    msgSaysImGoingToKillMyself = False
    msgSaysIWantToDie = False
    msgSaysImFeelingSuicidal = False
    msgSaysImFeelingQuiteSuicidal = False
    msgSaysIveBeenFeelingSuicidal = False
    msgSaysSuicidalThoughts = False
    msgSaysIDontWantToLive = False
    msgSaysShouldIKillMyself = False
    msgSaysImCrying = False
    msgSaysNothingToLiveFor = False
    msgSaysSingleWordDepression = False
    msgSaysFeelingDepressed = False
    msgSaysIHaveNoWayOut = False
    msgSaysHadEnoughOfLife = False
    msgSaysNothingToLookForwardTo = False
    msgSaysImUseless = False
    msgSaysImWorthless = False
    msgSaysFeelingLonely = False
    msgSaysDontHaveAnyoneICanTalkTo = False
    msgSaysIHateHowILook = False
    msgSaysFeelOverwhelmed = False
    msgSaysFeelingAwful = False
    msgSaysImAFailure = False
    msgSaysImALetdown = False
    msgSaysLetMyselfDown = False
    msgSaysFeelOutOfControl = False
    msgSaysFeelLost = False
    msgSaysInABadPlace = False
    msgSaysDeserve = False
    msgSaysIHateHowIFeel = False
    msgSaysImSad = False
    msgSaysFeelingLowDownTerrible = False
    msgSaysImUpset = False
    msgSaysImAddicted = False
    msgSaysFeelingRubbish = False
    msgSaysIHaveAnxiety = False # code using this is commented out currently
    msgSaysImAnxious = False # code using this is commented out currently
    msgSaysImWorried = False
    msgSaysIHaveAnxietyResponseAlreadyUsed = False
    msgSaysImAnxiousResponseAlreadyUsed = False
    msgSaysImWorriedResponseAlreadyUsed = False
    msgSaysIDontKnowWhatToDo = False
    msgSaysImNotHappy = False
    msgSaysIHateMyself = False
    msgSaysDifficultDay = False
    msgSaysFamilyProblems = False
    msgSaysFeelLost = False
    msgSaysDoYouGiveAdvice = False

    negatedString = ""


    def cleanText(message):
        """
        This function takes a string (e.g. the user's message) and cleans it to make it suitable for analysing.
        It does this by
        1. clean the string so that it only contains alphabetic characters and spaces (everything else is deleted)
        2. remove extraneous words (this results in a list)
        3. turn list back into string
        Cleaning the message makes the system more robust, because we've seen instances of triggers not getting recognised...
        ... we speculate that different treatments of the apostrophe character might be the reason.
        Note: Daniel has suggested that we do this more neatly with the below (ocmmented out) code. Have not implemented this yet.
        """

        ## NOTE Daniel suggested that this function could be implemented more neatly with the below code.
        ## NOTE I haven't gone through this yet, so it's in here (commented out) but could be implemented later
        #cleanedMessage = ["".join(list(filter(str.isalpha, i))) for i in message.split() if i not in extraneousWordsArray]
        #cleanedMessage = ' '.join(cleanedMessage)


        extraneousWordsArray = ["still", "just", "so", "very", "totally", "utterly", "really", "completely", "literally", "actually", \
        "even", "some", "always"]
        # I wanted to include "such a" in the extraneousWordsArray, but the current method does'nt work for that...
        #... because the current method "splits" the string into a list of separate words

        print("DEBUG: at start of clean text function, message = "+ message)

        # Step 1: clean the string so that it only contains alphabetic characters and spaces (everything else is deleted)
        messageCleanedOfCharacters = ""
        for char in message:
            if char.isalpha() or char == " ":
                messageCleanedOfCharacters = messageCleanedOfCharacters+char

        print("DEBUG: in clean text function, messageCleanedOfCharacters = "+ messageCleanedOfCharacters)

        # Step 2: remove extraneous words
        message_list = messageCleanedOfCharacters.split()
        # for word in message_list:
        #     if word in extraneousWordsArray:
        #         del word
        # for i in range(0,len(message_list)):
        #     print("DEWBUG: i = "+str(i)+" and message_list[i] = "+ message_list[i])
        #     if message_list[i] in extraneousWordsArray:
        #         del message_list[i]

        loopEnd = len(message_list)
        i = 0
        while i < loopEnd:
            print("DEWBUG: i = "+str(i)+" and message_list[i] = "+ message_list[i])
            if message_list[i] in extraneousWordsArray:
                del message_list[i]
                loopEnd = loopEnd - 1
                i = i - 1
            i = i + 1

        # Step 3: reconstruct string
        cleanedMessage = ""
        for word in message_list:
            cleanedMessage = cleanedMessage + word + " "

        print("DEBUG: at end of clean text function, cleanedMessage = "+ cleanedMessage)


        return cleanedMessage


    print("Prior to cleaning, the message is "+message)
    cleanedMessage = ""
    cleanedMessage = cleanText(message)
    print("After cleaning, we have claenedmessage = "+cleanedMessage)


    # The below cleaning method isn't be used any more
    # for char in message:
    #     if char.isalpha():
    #         cleanedMessage = cleanedMessage+char



    for string in iWantToKillMyselfArray:             # work out if anything from the iWantToKillMyselfArray is in the user's message
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "i Want To KillMyself" or similar
            msgSaysIWantToKillMyself = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIWantToKillMyself = False                                     # ... then set this flag to false
    for string in imGoingToKillMyselfArray:             # work out if anything from the imGoingToKillMyselfArray is in the user's message
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "i Want To KillMyself" or similar
            msgSaysImGoingToKillMyself = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImGoingToKillMyself = False                                     # ... then set this flag to false
    for string in iWantToDieArray:             # work out if anything from the iWantToDieArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "i Want To KillMyself" or similar
            msgSaysIWantToDie = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIWantToDie = False                                     # ... then set this flag to false
    for string in imFeelingSuicidalArray:             # work out if anything from the imFeelingSuicidalArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imfeelingsuicidal" or similar
            msgSaysImFeelingSuicidal = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImFeelingSuicidal = False                                     # ... then set this flag to false
                    print("negated string has been found and msgSaysImFeelingSuicidal has been set to false!!!!!!!!!!!!!!!!!!!")
    for string in iveBeenFeelingSuicidalArray:             # work out if anything from the iveBeenFeelingSuicidalArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "iveBeenFeelingSuicidal" or similar
            msgSaysIveBeenFeelingSuicidal = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIveBeenFeelingSuicidal = False                                     # ... then set this flag to false
    for string in imFeelingQuiteSuicidalArray:             # work out if anything from the imFeelingQuiteSuicidalArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imFeelingQuiteSuicidal" or similar
            msgSaysImFeelingQuiteSuicidal = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImFeelingQuiteSuicidal = False                                     # ... then set this flag to false
    for string in suicidalThoughtsArray:             # work out if anything from the suicidalThoughtsArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "suicidalThoughts" or similar
            msgSaysSuicidalThoughts = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysSuicidalThoughts = False                                     # ... then set this flag to false
    for string in iDontWantToLiveArray:             # work out if anything from the  IDontWantToLiveArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains " IDontWantToLive" or similar
            msgSaysIDontWantToLive = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIDontWantToLive = False                                     # ... then set this flag to false
    for string in shouldIKillMyselfArray:             # work out if anything from the ShouldIKillMyselfArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "ShouldIKillMyself" or similar
            msgSaysShouldIKillMyself = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysShouldIKillMyself = False                                     # ... then set this flag to false
    for string in nothingToLiveForArray:             # work out if anything from the nothingToLiveForArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "nothingToLiveFor" or similar
            msgSaysNothingToLiveFor = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysNothingToLiveFor = False                                     # ... then set this flag to false
    for string in imCryingArray:             # work out if anything from the imCryingArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imCrying" or similar
            msgSaysImCrying = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImCrying = False                                     # ... then set this flag to false
    for string in nothingToLiveForArray:             # work out if anything from the nothingToLiveForArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "nothingToLiveFor" or similar
            msgSaysNothingToLiveFor = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysNothingToLiveFor = False                                     # ... then set this flag to false
    for string in feelingDepressedArray:             # work out if anything from the feelingDepressedArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelingDepressed" or similar
            msgSaysFeelingDepressed = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelingDepressed = False                                     # ... then set this flag to false
    for string in feelingLonelyArray:             # work out if anything from the FeelingLonelyArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "FeelingLonely" or similar
            msgSaysFeelingLonely = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelingLonely = False                                     # ... then set this flag to false
    for string in iHateMyselfArray:             # work out if anything from the iHateMyselfArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "iHateMyself" or similar
            msgSaysIHateMyself = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIHateMyself = False                                     # ... then set this flag to false
    for string in iHaveNoWayOutArray:             # work out if anything from the iHaveNoWayOutArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "iHaveNoWayOut" or similar
            msgSaysIHaveNoWayOut = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIHaveNoWayOut = False                                     # ... then set this flag to false
    for string in hadEnoughOfLifeArray:             # work out if anything from the hadEnoughOfLifeArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "hadEnoughOfLife" or similar
            msgSaysHadEnoughOfLife = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysHadEnoughOfLife = False                                     # ... then set this flag to false
    for string in nothingToLookForwardToArray:             # work out if anything from the nothingToLookForwardToArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "nothingToLookForwardTo" or similar
            msgSaysNothingToLookForwardTo = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysNothingToLookForwardTo = False                                     # ... then set this flag to false
    for string in imUselessArray:             # work out if anything from the imUselessArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imUseless" or similar
            msgSaysImUseless = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImUseless = False                                     # ... then set this flag to false
    for string in imWorthlessArray:             # work out if anything from the imWorthlessArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imWorthless" or similar
            msgSaysImWorthless = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImWorthless = False                                     # ... then set this flag to false
    for string in dontHaveAnyoneICanTalkToArray:             # work out if anything from the dontHaveAnyoneICanTalkToArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "dontHaveAnyoneICanTalkTo" or similar
            msgSaysDontHaveAnyoneICanTalkTo = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysDontHaveAnyoneICanTalkTo = False                                     # ... then set this flag to false
    for string in iHateHowILookArray:             # work out if anything from the iHateHowILookArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "iHateHowILook" or similar
            msgSaysIHateHowILook = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIHateHowILook = False                                     # ... then set this flag to false
    for string in feelOverwhelmedArray:             # work out if anything from the feelOverwhelmedArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelOverwhelmed" or similar
            msgSaysFeelOverwhelmed = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelOverwhelmed = False                                     # ... then set this flag to false
    for string in feelingAwfulArray:             # work out if anything from the feelingAwfulArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelingAwful" or similar
            msgSaysFeelingAwful = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelingAwful = False                                     # ... then set this flag to false
    for string in imAFailureArray:             # work out if anything from the ImAFailureArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "ImAFailure" or similar
            msgSaysImAFailure = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImAFailure = False                                     # ... then set this flag to false
    for string in imALetdownArray:             # work out if anything from the ImALetdownArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "ImALetdown" or similar
            msgSaysImALetdown = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImALetdown = False                                     # ... then set this flag to false
    ## NOTE:  letMyselfDown is treated slightly differently. All the other strings start with I (i.e. the first person pronoun)
    ## "Let myself down" doesn't need to because it already contains a reflexive first person pronoun
    ## But this means that the preceding "it's not that" check needs to be more sophisticated.
    ## This is done further down.
    for string in feelOutOfControlArray:             # work out if anything from the feelOutOfControlArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelOutOfControl" or similar
            msgSaysFeelOutOfControl = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelOutOfControl = False                                     # ... then set this flag to false
    for string in feelLostArray:             # work out if anything from the feelLostArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelLost" or similar
            msgSaysFeelLost = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelLost = False                                     # ... then set this flag to false
    for string in inABadPlaceArray:             # work out if anything from the inABadPlaceArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "inABadPlace" or similar
            msgSaysInABadPlace = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysInABadPlace = False                                     # ... then set this flag to false
    for string in iHateHowIFeelArray:             # work out if anything from the IHateHowIFeelArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "IHateHowIFeel" or similar
            msgSaysIHateHowIFeel = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIHateHowIFeel = False                                     # ... then set this flag to false
    for string in imSadArray:             # work out if anything from the imSadArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imSad" or similar
            msgSaysImSad = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImSad = False                                     # ... then set this flag to false
    for string in feelingLowDownTerribleArray:             # work out if anything from the feelingLowDownTerribleArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelingLowDownTerrible" or similar
            msgSaysFeelingLowDownTerrible = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelingLowDownTerrible = False                                     # ... then set this flag to false
    for string in imUpsetArray:             # work out if anything from the imUpsetArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imUpset" or similar
            msgSaysImUpset = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImUpset = False                                     # ... then set this flag to false
    for string in imAddictedArray:             # work out if anything from the imAddictedArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imAddicted" or similar
            msgSaysImAddicted = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImAddicted = False                                     # ... then set this flag to false
    for string in feelingRubbishArray:             # work out if anything from the feelingRubbishArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "feelingRubbish" or similar
            msgSaysFeelingRubbish = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFeelingRubbish = False                                     # ... then set this flag to false
    for string in imAnxiousArray:             # work out if anything from the imAnxiousArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imAnxious" or similar
            msgSaysImAnxious = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImAnxious = False                                     # ... then set this flag to false
    for string in iHaveAnxietyArray:             # work out if anything from the iHaveAnxietyArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "iHaveAnxiety" or similar
            msgSaysIHaveAnxiety = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIHaveAnxiety = False                                     # ... then set this flag to false
    for string in imWorriedArray:             # work out if anything from the imWorriedArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imWorried" or similar
            msgSaysImWorried = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImWorried = False                                     # ... then set this flag to false
    for string in iDontKnowWhatToDoArray:             # work out if anything from the IDontKnowWhatToDoArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "IDontKnowWhatToDo" or similar
            msgSaysIDontKnowWhatToDo = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysIDontKnowWhatToDo = False                                     # ... then set this flag to false
    for string in imNotHappyArray:             # work out if anything from the imNotHappyArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "imNotHappy" or similar
            msgSaysImNotHappy = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImNotHappy = False                                     # ... then set this flag to false
    for string in familyProblemsArray:             # work out if anything from the familyProblemsArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "familyProblems" or similar
            msgSaysFamilyProblems = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysFamilyProblems = False                                     # ... then set this flag to false

    ## "Let myself down" is treated slightly different because it doesn't have a first person pronoun at the start, so the negating string is done differently
    for string in letMyselfDownArray:             # work out if anything from the letMyselfDownArray is in the user's cleanedMessage
        if string in cleanedMessage.lower():                          # if cleanedMessage contains "letMyselfDown" or similar
            msgSaysLetMyselfDown = True
            for negatingString in itsNotThatArray:
                negatedStringArray = [negatingString+string, negatingString+"i"+string, negatingString+"ive"+string, negatingString+"i've"+string] # including "i've" doesn't make sense any more now that we're using cleanedMessage, which takes the punctuation out anyway
                for negatedString in negatedStringArray:
                    if negatedString in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it, or "it's not that i" before it, or ...
                        msgSaysLetMyselfDown = False                                     # ... then set this flag to false

    ## "Do you give advice" is trated differently ebcause there's no need to include the negatig string check
    for string in doYouGiveAdviceArray:             # work out if anything from the doYouGiveAdviceArray is in the user's message
        if string.replace(" ","") in cleanedMessage.lower().replace(" ",""):                          # if message contains "do you give advice" or similar
            msgSaysDoYouGiveAdvice = True

    ## This section is another way of checking if msgSaysNothingToLiveFor shuld be true.
    ## It works by going through each of hte words "have anything to live for" and checking
    ## (a) is each of those words in the user's message?
    ## (b) do they appear in the right order? (this is a slightly hacky way of checking that)
    ## if both (a) and (b) apply, then this also sets msgSaysNothingToLiveFor to True
    haveAnythingToLiveFor = "have anything to live for"
    wordInMessage = []
    for word in haveAnythingToLiveFor.lower().split():
        if word in cleanedMessage.lower():
            wordInMessage.append(True)
        else:
            wordInMessage.append(False)
    allWordsInMessage = all(wordInMessage)
    wordsInRightOrderBool = False # initialising
    if allWordsInMessage:
        wordsInRightOrderArray = []
        for i in len(haveAnythingToLiveFor.lower().split()):
            if i == 0: # if it's the first word in the array
                wordsInRightOrderArray[i] = True
            else:
                if message.index(haveAnythingToLiveFor.lower().split()[i]) > message.index(haveAnythingToLiveFor.lower().split()[i-1]):
                #if the lowest index where the ith word is found is after the lowest index where the (i-1)th index is found
                #I actually don't think this is quite the logic I want, but I do'nt want to let the perfect be the enemy of the good
                    wordsInRightOrderArray[i] = True
                else:
                    wordsInRightOrderArray[i] = False
        wordsInRightOrderBool = all(wordsInRightOrderArray)

    if allWordsInMessage and wordsInRightOrderBool:
        msgSaysNothingToLiveFor = True
    ## This is the end of the section that is another way of checking if msgSaysNothingToLiveFor shuld be true.


    # debug
    print("message ="+str(message))


    def selectRandomResponse():
        ### If none of the triggers is hit, the backup option is to select a random encouraging Noise.
        ### This function is to select that encouraging noise
        randomlyChosenIndex = random.randint(0,noOfEncouragingNoises-1)
        response = encouragingNoises[randomlyChosenIndex]
        return response



    if msgSaysIWantToKillMyself == True and iWantToKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I want to kill myself"
        print("This is inside the if msgSaysIWantToKillMyself == True and... statement")
        response = "Things must be pretty grim if you've got to the stage where you're talking about ending your life like this."
        iWantToKillMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImGoingToKillMyself == True and imGoingToKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm going to kill myself", then if the user has indicated that they are feeling suicidal
        # then treat the users statement that they will kill themself as a statement of serious suicidal intent.
        # However if it's not accompanied by suicidal language, then it's not so clear, e.g. some users have said things like
        # "i'm going to kill myself with all the alcohol i'm consuming"

        #if CALLER IS SUICIDAL
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True]
        if userIsSuicidal:
            response = "You say that you're going to kill yourself. I'm saddened to hear that. Could you say more about death and what it means for you?"
        else:
            response = "It sounds pretty stark to hear you say that you will kill yourself."

        imGoingToKillMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantToDie == True and iWantToDieResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I want to kill myself"
        response = "I'm sorry to hear you say that you want to die."
        iWantToDieResponseAlreadyUsed = [conversationId,True]
    elif (msgSaysImFeelingSuicidal == True or msgSaysIveBeenFeelingSuicidal == True) and imFeelingSuicidalResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm feeling suicidal"
        # note that the response is very similar to the "feeling quite suicidal" response, so these two use the same imFeelingSuicidalResponseAlreadyUsed variable
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you mention that you're feeling suicidal. Could we perhaps explore that a bit more?"
        else:
            response = "I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling suicidal. I'm sorry to hear that. Could you tell me more about those feelings?"
        imFeelingSuicidalResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImFeelingQuiteSuicidal == True and imFeelingSuicidalResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm feeling quite suicidal"
        # note that the response is very similar to the "feeling suicidal" response, so these two use the same imFeelingSuicidalResponseAlreadyUsed variable
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you mention that you're feeling suicidal. Do you feel this way often?"
        else:
            response = "I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling quite suicidal. I'm sorry to hear that. Could you tell me more about those feelings?"
        imFeelingSuicidalResponseAlreadyUsed = [conversationId,True]

    elif msgSaysSuicidalThoughts == True and suicidalThoughtsResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        if len(message) < 40:
            response = "I'm sorry to hear that. Could you tell me more about these suicidal thoughts?"
        else:
            response = "You just mentioned suicidal thoughts. If you have anything more to say about that, I'd be happy to hear?"
        suicidalThoughtsResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIDontWantToLive == True and iDontWantToLiveResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts or msgSaysShouldIKillMyself \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True] or shouldIKillMyselfResponseAlreadyUsed == [conversationId,True]
        if userIsSuicidal:
            if USER_CHARACTER_COUNT < 300:
                response = "I'm hearing loud and clear that you don't want to be alive, and it's really sad that it's got to this. Could you say any more about what's making you feel this way?"
            else:
                response = "It's sad that you're feeling that you don't want to be alive any more, and that you want to die."
        else: # i.e. if we haven't picked up any other clear indications of suicidality
            if USER_CHARACTER_COUNT < 300:
                response = "I'm sorry to hear you say that you don't want to live. If you want to explore your thoughts about this, including thinking through any suicidal thoughts you have, feel free to use me as a sounding board"
            else:
                response = "It's so sad that it's got to the stage where you feel that way about your life."
        iDontWantToLiveResponseAlreadyUsed = [conversationId,True]


    elif msgSaysShouldIKillMyself == True and shouldIKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "hsould i kill myseld"
        if message.lower() in shouldIKillMyselfArray or message.lower()[:len(message)-1] in shouldIKillMyselfArray: # if the user's message is exactly equal to one of the things in the array (or perhaps just has a question mark or somtehing at the end), then we have more confidence that they are actually asking this question
            if USER_CHARACTER_COUNT < 300:
                response = "The fact that you are asking this question means that things must be really bad for you. I'm sorry that you're feeling this way. Can you say more about how you're feeling?"
            else:
                response = "The fact that you are asking this question means that things must be really bad for you. I'm sorry that you're feeling this way."
        else: # if the string isn't equal to "should i kill myself" or similar, then we have to phrase the response a bit more cautiously
            if USER_CHARACTER_COUNT < 300:
                response = "If anyone even thinks about ending their life, then things must be really bad. I'm sorry for your suffering. Can you tell me more about what's making you feel this way?"
            else:
                response = "If anyone even thinks about ending their life, then things must be really bad. I'm sorry for your suffering. Can you say more about what you think you should do?"

        shouldIKillMyselfResponseAlreadyUsed = [conversationId,True]




    elif msgSaysImCrying == True and cryingResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = "I'm sorry to hear that you're feeling this way, and that it's making you cry. That sounds so sad."
        cryingResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNothingToLiveFor == True and nothingToLiveForResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i have nothing to live for"

        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True]

        if userIsSuicidal:
            response = "It sounds bleak to hear you say you have nothing to live for, and I find it sad that you've been expressing suicidal thoughts."
        else:
            response = "I'm sorry to hear you say that you have nothing to live for. You saying that makes me worry about \
            whether you want to continue to live, or if you're having suicidal thoughts. Could you say more about what's on your mind?"
        nothingToLiveForResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHateMyself == True and iHateMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i hate myself"
        if USER_CHARACTER_COUNT < 1000:
            response = "I think it's really sad to hear you say that you hate yourself. Could you say a bit more about why you have this low self-esteem?"
        else:
            response = "I think it's really sad to hear you say that you hate yourself."
        iHateMyselfResponseAlreadyUsed = [conversationId,True]

    elif message.lower() in singleWordDepressionMessageArray and USER_CHARACTER_COUNT < 40 and singleWordDepressionResponseAlreadyUsed != [conversationId,True]:
        ### If the user gives a single word message saying "depression" or "depressed" or similar early in the conversation, ask to explore that further
        #This version was designed with follow-up comments in mind, but the codebase isn't ready for followup comments, so this version remains commented out for now
        #response = "OK, so I see you have depression on your mind. Are you feeling depressed?"
        # Maybe add some follow-up comments here, e.g. if the user says yes, then reply with "have you feeling this way for a long time?" and then ...
        response = "OK, so I see you have depression on your mind. Are you feeling depressed? Maybe you could share a bit more about this with me?"
        singleWordDepressionResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingDepressed == True and feelingDepressedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling depressed", then reply with
        response = "Sorry to hear you're feeling depressed. Would you like to tell me more about that?"
        feelingDepressedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHaveNoWayOut == True and iHaveNoWayOutResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "IHaveNoWayOut", then reply with
        response = "I heard you mentioned that you feel you have no way out. Do you feel trapped?"
        iHaveNoWayOutResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHadEnoughOfLife == True and hadEnoughOfLifeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "HadEnoughOfLife", then reply with
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True]

        if userIsSuicidal:
            response = "So I've heard you say that you're feeling suicidal, and you're saying that you've had enough of life. I'm sorry it's got to the stage where you're feeling this way."
        else:
            response = "I'm sorry to hear you say that you've had enough of life. Sometimes when people say that they are also having suicidal thoughts..."

        hadEnoughOfLifeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNothingToLookForwardTo == True and nothingToLookForwardToResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "NothingToLookForwardTo", then reply with
        response = "It sounds quite bleak to hear you say that you have nothing to look forward to"
        nothingToLookForwardToResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImUseless == True and imUselessResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm useless", then...
        if USER_CHARACTER_COUNT < 1000:
            response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you. Could you say more about what's making you say this?"
        else:
            response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you."
        imUselessResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImWorthless == True and imWorthlessResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm worthless", then reply with
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you say that you're worthless. Could you say more about what's on your mind?"
        else:
            response = "I'm sorry to hear you say that you're worthless. You might want to place a bit less value on what I'm going to say now, because (a) I don't know you and (b) I'm really only a very unintelligent bot that doesn't understand everything, but I don't think you're worthless. For what it's worth."
        imWorthlessResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingLonely == True and feelingLonelyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling lonely", then reply with
        ### a response that varies depending on whether we are early in the conversation or not
        feelingLonelyResponseEnding = ""
        if USER_CHARACTER_COUNT < 500:
            feelingLonelyResponseEnding = ". Can you tell me more about this?"
        else:
            feelingLonelyResponseEnding = "."
        response = "Feeling connected to other people is such a fundamental human need. It's sad to hear you talk about this loneliness"+feelingLonelyResponseEnding
        feelingLonelyResponseAlreadyUsed = [conversationId,True]


    elif msgSaysDontHaveAnyoneICanTalkTo == True and dontHaveAnyoneICanTalkToResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "It's a shame that you feel you don't have anyone you can talk to. It sounds really isolating."
        dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIHateHowILook == True and iHateHowILookResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "IHateHowILook", then reply with
        response = "That sounds really tough. Could you say more about your thoughts on your looks?"
        iHateHowILookResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelOverwhelmed == True and feelOverwhelmedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelOverwhelmed", then reply with
        if USER_CHARACTER_COUNT < 100:  # if it's early in hte conversation
            response = "There must be a lot going on for you to be feeling overwhelmed like that. Would you like to tell me more?"
        elif USER_CHARACTER_COUNT < 500:
            response = "That sounds like a lot to deal with. I'm sorry it's got to the stage where it's making you feel overwhelmed."
        else: # by this stage (i.e. for a user_character_cout this high) the user has probably explained a lot of what's happened to make them feel overwhelemed
            response = "That all sounds like a lot to deal with. "
        feelOverwhelmedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingAwful == True and feelingAwfulResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelAwful", then reply with
        response = "I'm sorry to hear you're feeling so awful. If you think sharing more about that with me might help you feel less awful, I'm here to be a space for you to talk."
        feelingAwfulResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImAFailure == True and imAFailureResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I@m a failrure", then reply with
        response = "It's sad to hear you call yourself a failure. I'd love to tell you all the reasons why you're actually really awesome, but I don't know you (and I'm only a very simple bot) so I can't do that. But I do think everyone is valuable in their own way."
        imAFailureResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImALetdown == True and imALetdownResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I@m a letdown", then reply with
        response = "Now I'm hearing you call yourself a letdown, and I think that's sad. I'm here to listen to you about that, without judging."
        imALetdownResponseAlreadyUsed = [conversationId,True]

    elif msgSaysLetMyselfDown == True and letMyselfDownResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "You mentioned feeling that you had let yourself down. I hope you feel able to share with me some more thoughts about that, knowing that this is a place where you can talk without being judged."
        letMyselfDownResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelOutOfControl == True and feelOutOfControlResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelOutOfControl", then reply with
        response = "Can you say a bit more about these out of control feelings?"
        feelOutOfControlResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelLost == True and feelLostResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "Feel lost", then reply with
        if len(message) < 28: # if the message is about long enough to say "I'm feeling really lost", and not much longer than that:
            response = "You're saying that you're feeling lost, can you say more about that?"
        else:
            response = "That sounds like a very lost, forlorn feeling."
        feelLostResponseAlreadyUsed = [conversationId,True]

    elif msgSaysInABadPlace == True and inABadPlaceResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "In a bad place", then reply with
        if USER_CHARACTER_COUNT < 500:
            response = "You said you're in a bad place. Would you like to say more about that?"
        else:
            response = "I'm sorry to hear you say you're in a bad place."
        inABadPlaceResponseAlreadyUsed = [conversationId,True]


    elif (" i deserve" in message.lower() or message.lower()[:9] == "i deserve") and deserveResponseAlreadyUsed != [conversationId,True]:
        ### This is a bit of a risky one. However at time of writing, whenever I've seen a user write "i deserve",
        ### it's always been in a negative sense (e.g. "I deserve this suffering") and never (e.g.) "i deserve better"
        ### However if someone did write "i deserve better", I still think this response is ok
        ### Note the logic in hte if statement: if the message contains " i deserve" (starting with a space character)
        ### or if it starts with "i deserve". This means that a string like "naomi deserves" wouldn't trigger this reply
        response = "I just want to take a moment to assert that you are a valuable human being in your right, \
        no matter what"
        deserveResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIHateHowIFeel == True and iHateHowIFeelResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I hate how i feel", then reply with
        if USER_CHARACTER_COUNT < 300:             # if it's early in the conversation
            response = "I'm sorry to hear you say that you hate how you feel. Could you say more about these feelings?"
        else:
            response = "I'm sorry to hear you say that you hate how you feel."
        iHateHowIFeelResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImSad == True and imSadResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm sad", then reply with
        response = "Thank you for sharing with me the sadness you're experiencing."
        imSadResponseAlreadyUsed = [conversationId,True]


    elif msgSaysFeelingLowDownTerrible == True and feelingLowDownTerribleResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling low/down/terrible", then reply with
        response = "Sorry to hear you're feeling low."
        feelingLowDownTerribleResponseAlreadyUsed = [conversationId,True]


    elif msgSaysImUpset == True and imUpsetResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling upset", then reply with
        response = "Sorry that you're upset. Could you say a bit more about that?"
        imUpsetResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImAddicted == True and imAddictedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm addicted", then reply with
        response = "Addictions can be really tough. Could you say more about what it means for you?"
        imAddictedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingRubbish == True and feelingRubbishResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling rubbish", then reply with
        response = "Sorry that you're feeling rubbish. Could you say a bit more about that?"
        feelingRubbishResponseAlreadyUsed = [conversationId,True]


### I WAS GOING TO INCLUDE SOME RULES FOR "i have anxiety" AND "I'm anxious" BUT ON SECOND THOUGHTS I'M LEAVING THIS BE FOR NOW
### LOOKING BACK AT PAST USER BEHAVIOUR, WHEN USERS SAYS THIS IT TENDS TO BE IN COMPLEX SITUATIONS WHERE THERE IS ALSO LOTS OF OTHER SUTFF GOING ON
### SO I THINK IT BEST TO LEAVE THIS FOR NOW AND ANALYSE FURTTHER WHEN WE HAVE A BETTER IDEA OF HOW TO RESPOND

    # elif msgSaysIHaveAnxiety == True and iHaveAnxietyResponseAlreadyUsed != [conversationId,True]:
    #     ### If the message includes a string roughly equivalent to saying "I have anxiety", then reply with
    #     response = "I understand you suffer from anxiety. Could you tell me more about your feelings right now?"
    #     iHaveAnxietyResponseAlreadyUsed = [conversationId,True]
    #
    #
    # elif msgSaysImAnxious == True and imAnxiousResponseAlreadyUsed != [conversationId,True]:
    #     ### If the message includes a string roughly equivalent to saying "I'm anxious", then reply with
    #     response = "Sorry that you're feeling anxious. Could you say a bit more about that?"
    #     imAnxiousResponseAlreadyUsed = [conversationId,True]


    elif msgSaysImWorried == True and second_imWorriedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm worried"
        ### This rule covers 2 scenarios: either we're early in the converation or not so early
        ### If we're early, then second_imWorriedResponseAlreadyUsed can't be true for this conversation,
        ### so the if statement above just refers to second_imWorriedResponseAlreadyUsed only

        if USER_CHARACTER_COUNT < 100: # if its early in the conversation
            if initial_imWorriedResponseAlreadyUsed != [conversationId,True]:
                response = "Can you tell me more about what you're worried about?"
                initial_imWorriedResponseAlreadyUsed = [conversationId,True]
            else:
                # I'm giving here several responses for the bot to choose at random.
                # This is because conceivably a user might type "I'm worried" several times within hte first 100 characters
                earlyWorriedResponses = ["I'm sorry to hear that you're feeling these worries.",
                                        "Feeling worried like this must be tough for you.",
                                        "Thank you for sharing the worries you're feeling. I'm here to listen.",
                                        "It's a shame these worries are affecting you like this."]
                randomlyChosenIndex = random.randint(0,len(earlyWorriedResponses)-1) # select a random number between 0 and final index of the earlyWorriedResponses array
                response = earlyWorriedResponses[randomlyChosenIndex] # set the response equal to the string (or whatever) corresponding to the relevant index
        else:                         # if it's not that early in the conversation
            response = "I'm sorry to hear about all these worries you're experiencing"
            second_imWorriedResponseAlreadyUsed  = [conversationId,True]

        imWorriedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIDontKnowWhatToDo == True and iDontKnowWhatToDoResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling rubbish", then reply with
        response = "So you said you're not sure what to do. Can you think of any options that you would like to explore with me?"
        iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,True]

    elif message.lower() in iDontKnowWhatToSayArray:
        ### If the message is equal to a string roughly equivalent to saying "I do'nt know what to say", then reply with
        if USER_CHARACTER_COUNT < 200:
            if initial_iDontKnowWhatToSayResponseAlreadyUsed != [conversationId, True]:
                response = "This is a space for you to talk about what you're feeling. I'm guessing if you've ended up \
                at this site you're feeling low. Would you like to say more about that?"
                initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, True]
            else:
                response = "Sorry if it sounds like I'm repeating myself, but this is a space for you to explore whatever's on \
                your mind. Would you like to tell me a bit about how you're feeling?"
        else:
            if second_iDontKnowWhatToSayResponseAlreadyUsed != [conversationId, True]:
                response = ["Thank you for having shared the things you've shared thus far. Perhaps let's just pause for a moment \
                and think about how you're feeling right now.", "Having thought about that for a moment, can you think of anything \
                that's on your mind that would be useful to discuss?"]
                second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId,True]
            else:
                response = ["I realise you've asked me this before, and I'm just going to say the same thing again (I'm a very unimaginative bot!) \
                Perhaps let's just pause for a moment \
                and think about how you're feeling right now.", "Having thought about that for a moment, can you think of anything \
                that's on your mind that would be useful to discuss?"]
        iDontKnowWhatToSayResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImNotHappy == True and imNotHappyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm not happy", then reply with
        response = "You said that you're not feeling happy. That's sad. "
        imNotHappyResponseAlreadyUsed = [conversationId,True]

    elif message.lower() in difficultDayArray and difficultDayResponseAlreadyUsed != [conversationId,True]:
        ### If the user's message is equal to "i've had a difficult day" (or a synonym in the array) then give this response
        response = "Could you tell me more about the difficult day you've been having?"
        difficultDayResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFamilyProblems == True and familyProblemsResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "Could you tell me more about these family difficulties?"
        familyProblemsResponseAlreadyUsed = [conversationId,True]

    elif section == 11 and message.lower() in helloArray:
        ### if the user says hello
        response = "Hi! :-) I'm here to listen. Would you like to talk about what's on your mind?"

    elif msgSaysDoYouGiveAdvice == True and doYouGiveAdviceResponseAlreadyUsed != [conversationId,True]:
        ### if the user asks if the bot gives advice
        adviceResponses = [["This bot is a safe, non-judgemental space to explore what's on your mind. Giving advice isn't part of \
        what I offer.", "Some people prefer not to be advised -- being told what to do can be disempowering, and talking \
        things through can help. But if advice is what you're after then I'm sorry not to be able to help. Would \
        you like to talk about what's on your mind?"], "This bot isn't about me advising you; it's about you talking and finding your own way through things. You're welcome to continue talking if that would help?"]
        randomlyChosenIndex = random.randint(0,len(adviceResponses)-1) # select a random number between 0 and final index of the adviceResponses array
        response = adviceResponses[randomlyChosenIndex] # set the response equal to the string (or whatever) corresponding to the relevant index
        doYouGiveAdviceResponseAlreadyUsed = [conversationId,True]


    elif section == 11 and len(message) < 10 or " " not in message :
        ### If it's the user's first written response and they've given  (essentially) a one-word message
        ### When I say one-word message, I mean that either it has no space characters in it, or something that might be longer but has no space characters (this includes someone typing gibberish)
        ### Note that any space-character-free message will get this response, whereas a short response will only hear this if it's the first message
        ### NOTE: HARDCODING THE NUMBER 11 IS BAD PRACTICE! SHOULD UPDATE THIS LATER!!!!!!!!!!!!!11
        response = "I see you've said something very short there, which is cool :-). But feel free to type full sentences if you want. Just write about whatever's on your mind -- I'm here to listen."

    elif section == 11 and " feeling " in message.lower():
        ### If it's the user's first written response and it includes hte word "feeling" then the response is...
        ### NOTE: HARDCODING THE NUMBER 11 IS BAD PRACTICE! SHOULD UPDATE THIS LATER!!!!!!!!!!!!!11
        response = "Thank you for sharing this. Could you tell me more about your feelings please?"

    elif message.lower() in stopSynonymsArray:
        ### If the user is saying something that seems to suggest they want to stop using the botText
        ### Note: most other responses are set up to not be repeated if already used, but I think this one can be repeated
        ### Because it's possible that this could come up more than once, multiple possible responses are coded
        responsesToStopMessages = ["Sorry I'm such a simple bot and I'm not understanding you very well, but \
        are you saying you want to stop using this bot? If so, would you mind clicking on the stop button on the side?",\
        "Thank you. I think you're telling me you want to stop this conversation (sorry if I misunderstood!) If so, could \
        you please click the stop button?",\
        "If I'm understanding you right, you're telling me you want to stop now. Please feel free to click the stop button, \
        or if you want to continue using this bot, just continue talking", "Are you saying you want to stop using this bot? If so, \
        would you mind clicking on the stop button on the side? (or you can just keep talking, of course)", "I think you're telling me \
        you want to stop now (but I could be \
        wrong because I'm a very simple bot). If that's right, could you click the stop button?"]
        randomlyChosenIndex = random.randint(0,len(responsesToStopMessages)-1) # select a random number between 0 and final index of the responsesToStopMessages array
        response = responsesToStopMessages[randomlyChosenIndex] # set the response equal to the string corresponding to the relevant index

    else:
        response = selectRandomResponse()

    return response


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/get")
def get_bot_response():
    time.sleep(1)
    _input = json.loads(request.args.get('msg'))
    message = _input[0]
    global section
    section = _input[1]
    output = _input[2] # I don't know what this is for!
    score = _input[3]
    initialHappinessScore = int(_input[4])
    finalHappinessScore = int(_input[5])
    anonymous = _input[6]
    global conversationId
    conversationId = _input[7]
    start_again = False
    global USER_CHARACTER_COUNT
    nextUserInput = ""
    nextUserInputFreeText = "<input id='textInput' type='text' name='msg' placeholder='Message' />" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
    nextUserInputYesNo = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    <option value='no'>No</option> \
    </select>"
    nextUserInputOneOption = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    </select>"
    nextUserInputTwoOptions = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    <option value='no'>No</option> \
    </select>"
    nextUserInputFinalHappinessSurvey = "<select type='number' id='finalHappinessSurvey' onchange='getBotResponse()'>\
<option>Select</option>\
<option name='finalHappinessValue' value=1>1</option>\
<option name='finalHappinessValue' value=2>2</option>\
<option name='finalHappinessValue' value=3>3</option>\
<option name='finalHappinessValue' value=4>4</option>\
<option name='finalHappinessValue' value=5>5</option>\
<option name='finalHappinessValue' value=6>6</option>\
<option name='finalHappinessValue' value=7>7</option>\
<option name='finalHappinessValue' value=8>8</option>\
<option name='finalHappinessValue' value=9>9</option>\
<option name='finalHappinessValue' value=10>10</option>\
</select>"

    nextUserInputType = "initialHappinessSurvey" # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputType in the javascript code

    print("This si the get_bot_response function")

    if section==1:

        if initialHappinessScore > 7:
            response = "Sounds like you're feeling OK! I'm designed for people who are feeling low \
            and have something on their mind. But that's cool, let's talk anyway! :-) \
            Can I tell you first how this bot works?"
        elif initialHappinessScore > 3:
            response = "Thanks for sharing. I'm going to ask you to talk about whatever is on your \
            mind, but first I'm going to explain how this bot works, is that OK?"
        else:
            #response = "Oh dear, sounds like you're feeling really low, I'm sorry to hear that. \
            #I want to ask you more about that, but first can I tell you how this bot works?"
            response = ["Oh dear, sounds like you're feeling really low, I'm sorry to hear that",
            "I want to ask you more about that, but first can I tell you how this bot works?"]

        noOfResponseFragments = 0 # to assign the variable
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, happy to listen to the explanation of how this bot works")
        nextUserInputType = "userInputButton"
        next_section = section + 1
        #next_section = 9 # DEBUG CHEAT: for debugging purposes when you want to skip the intro. This shouldn't apply normally

        # The next few lines prepares some inputs for the write_data function
        conversationId = str(datetime.now())
        initialiseResponseAlreadyUsedVariables()
        responseIndex = 0 # I don't think this declaration is needed
        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, "initialHappinessScore (!!) = "+message, responseForWriteData)


    elif section==2:

        response = ["I'm actually a very simple little bot. So please feel free to talk to me, \
        and sorry in advance if I don't always do a good job of understanding you.",
        "Instead think of this as being more like writing a journal, but as you keep writing, \
        I'll be here to encourage you to keep talking."]

        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I will talk with you even though you are a simple bot.")
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData)


    elif section==3:

        response = "Now let's talk about confidentiality and anonymity. \
        We offer an anonymised service. We don't have any way \
        of tracking you down, knowing who you are, or linking what you write to you."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I understand that you do not know who I am.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==4:

        response = "So given that I can't track you down, and also because I'm a very simple bot, \
        if you told me about an emergency/crisis situation, I wouldn't \
        be able to help."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know you cannot provide emergency services.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==5:

        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
        or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
        us improve the way this software works, but we still won't know who you are."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know what you mean by anonymous.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==6:

        response = "And when I say confidential, I mean that your text won't be \
        stored at all, and no human will see what you write."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know what you mean by confidential.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==7:

        response = "Would you like this service to be anonymous or confidential?"
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_two("Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==8:

        anonymous = "true" if message.split()[0].lower()=="anonymous" else "false"
        response = "Thanks! One last thing: You remember saying how you felt on a scale from 1 to 10 \
        at the start? I'd like to ask you the same thing at the end so I know if we're helping."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, I am happy to let you see how I feel at the end too")
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response)

    elif section==9:

        response = ["When you're finished using the bot, please click the stop button on the right\
        or just type 'stop'; this will take you to the super-quick final survey.", "Don't press it now, but \
        can you press this button instead of closing/exiting this window?"]
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, when I am finished I will click the stop button")
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData)


    elif section==10:

        responseFragmentBasedOnScore =""

        if initialHappinessScore > 7:
            responseFragmentBasedOnScore = "Seems like you're feeling OK, but I'm still available for you \
            to chat with if you want. Maybe just start by talking about something that's on your mind?"
        elif initialHappinessScore > 3:
            responseFragmentBasedOnScore = "Would you like to start by talking about something that's on your mind?"
        else:
            responseFragmentBasedOnScore = "Sounds like things are tough for you just now. Would you like to \
            start talking about something that's on your mind?"

        response = "OK, now we've got the intro stuff out the way... you were saying before that \
        you were feeling "+str(initialHappinessScore)+" out of 10. "+responseFragmentBasedOnScore

        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"

        write_data(anonymous, conversationId, message, response)




    elif section > 10:

        """
# This section was here and used textblob nlp. However it seem to be causing errors when using this locally on my laptop so I took it out
        try:
            sentence = TextBlob(message)
            score = sentence.sentiment.polarity
        except:
            score = 0

        responses = ["Sounds like things are really rough at the moment. Can I ask what is making you feel this way?", \
        "Sounds like things are not too easy at the moment. Can I ask what is making you feel this way?", \
        "Sounds like things could be a bit better. Can I ask what is making you feel this way?", \
        "To me it sounds like things are going ok for you, but I may be mistaken! Would you like to tell me more about it?"]
        response = responses[bisect_left(scores, score)]
        #next_section = 4
        """


# the bot gives an answer based on textblob. they carry on talking...
#    elif section == 4:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "That's ok. Would you like to talk about something else?"
#            next_section = 6
#        else:
#            responses = ["Sounds like things are really rough at the moment. Can I ask what is making you feel this way?", \
#            "Sounds like things are not too easy at the moment. Can I ask what is making you feel this way?", \
#            "Sounds like things could be a bit better. Can I ask what is making you feel this way?", \
#            "To me it sounds like things are going ok for you, but I may be mistaken! Would you like to tell me more about it?"]
#            response = responses[bisect_left(scores, score)]
#            next_section = 5
#
#    # this is the section of encouraging noises
#    elif section == 5:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "Ok, Is there anything else you would like to talk about?"
#            next_section = 6
#        else:
#            responses = ["Go on, I'm still listening", "Can you say more about that?"]
#            response_num = 1 if random.uniform(0, 1)>0.5 else 0
#            response = responses[response_num]
#            next_section = 5
#
#    # this is the section to gauge how they're feeling on a scale from 1 to 10
#    elif section == 6:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "Ok thanks for speaking to me. Have you found talking useful?"
#            next_section = 7
#        else:
#            responses = ["Go on, I'm still listening", "Can you say more about that?"]
#            response_num = 1 if random.uniform(0, 1)>0.5 else 0
#            response = responses[response_num]
#            next_section = 5
#    elif section == 7:
#        get_response = get_yes_no(message, ("That's great! I'm glad to hear it. \
#        Do you have any suggestions about how I could improve?",1),
#        ("Sorry to hear that. Do you have any suggestions about how I can improve?",1), \
#        ("Sorry I didn't understand that",0), section)
#        response = get_response[0]
#        next_section = get_response[1]
#    elif section == 8:
#        words = [i.lower() for i in message.split()]
#        if words[0]=="no" or " ".join(words[:2])=="not really" or " ".join(words[:3])=="i'd rather not":
#            response = "Ok thanks anyway. Do chat again if you'd like to"
#        else:
#            response = "Thanks for the feedback. Do chat again if you'd like to"
#        next_section=0

        USER_CHARACTER_COUNT += len(message)

        if(message.lower()=="stop"):
            response = "Thank you for using this bot. Please rate how you feel on a scale \
            from 1 to 10, where 1 is terrible and 10 is great. As a reminder, the score you \
            gave at the start was "+str(initialHappinessScore)
            next_section = -1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserInput = nextUserInputFinalHappinessSurvey
            nextUserInputType = "finalHappinessSurvey"
        else:
            #randomlyChosenIndex = random.randint(0,noOfEncouragingNoises-1)
            #response = encouragingNoises[randomlyChosenIndex]
            response = choose_bot_wordy_response(message)
            next_section = section + 1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserInput = nextUserInputFreeText
            nextUserInputType = "freeText"

        responseForWriteData = ""

        if isinstance(response,str):
            responseForWriteData = response
        elif isinstance(response, list):
            for responseIndex in range(0,noOfResponseFragments):
                responseForWriteData = responseForWriteData + response[responseIndex]

        write_data(anonymous, conversationId, message, responseForWriteData)


    elif section == -1: # this is the "end" (i.e. user has entered "stop") section

        # at the moment when the bot sensed that the user had entered "stop", it already immediately asked the final survey question

        happinessChange = finalHappinessScore - initialHappinessScore

        if happinessChange < 0:
            response = "Oh no! I'm so sorry you're feeling worse than you were at the start! :-(. \
            Please tell us why we made things worse, and what we could do better in future"
        elif happinessChange == 0:
            response = "We wanted to make things better for you, sorry you're feeling no better than \
            you did at the start. Optional final question - Please tell us whether we met your \
            expectations, and any suggestions for improvement."
        elif happinessChange > 0:
            response = "I'm glad you're feeling better than you did at the start. Optional final question: \
            if you have any comments to help us improve this bot, please make them here"

        next_section = -2
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"


        write_data(anonymous, conversationId, "finalHappinessScore (!!) = "+message, response)


    elif section == -2: # this is the "end" (i.e. user has entered "stop") section

        response="This is the end. Thank you for using the Talk It Over chatbot."
        #print("The response variable has just been set equal to "+response)

        next_section = -3
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = ""
        nextUserInputType = ""

        # output data
        #if anonymous=="true"
        dataToStore.append([message,response])

            #writer = csv.writer(f)
            #writer.writerow(dataToStore)

        #f = open("storedData.csv","w")
        #for i in range(0,len(dataToStore)):
        #f.write("\n" + str(dataToStore))
        #f.close()

        write_data(anonymous, conversationId, message, response)

    #time.sleep(min(sleep_per_word*len(response.split()), 2))  # this delay is meant to represent the bot's thinking time. I'm just finding it annoying, but perhaps if there's a better dancing ellipsis to represent typing, it might be more worthwhile having the delay in.
    print("This is the data which gets sent to the client side")
    print([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId])
    return make_response(dumps([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId]))




if __name__ == "__main__":
    app.run()

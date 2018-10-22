"""search and match intents, templates and actions"""

import os
import yaml
import pprint as pp
import argparse 
from sys import exit

#init
nluIntentList = []
domainIntentList = []
domainActionsList = []
domainTemplatesList = []
domainEntitiesList = []
domainSlotsList = []
nluEntityList = []
domainTemplatesFull = []
domainTemplatesSubEntities = []
storyEntityList = []
preprocessList = []

boolIntentsOK = True
boolActionsTemplatesOK = True
boolEntSlotOK = True

exitOK = True

PATH = os.getcwd() + os.sep

def create_argument_parser():
    parser = argparse.ArgumentParser(
            description='inspect nlu.md and domain.yml  data for consistency. Compare intents, entities, slots and templates.')

    parser.add_argument('-n', '--nlu',
                        default=PATH+'data'+os.sep+'nlu'+os.sep+'nlu.md',
                        help="Path to the nlu file")


    parser.add_argument('-d', '--domain',
                       default= PATH + 'domain.yml',
                       help="Path to the domain file")

    parser.add_argument('-s', '--story',
                        default=PATH+'data'+os.sep+'core'+os.sep+'stories.md',
                        help='Path to the story file')
    return parser


def comparison(listA, listB, labelA, labelB, fileA, fileB):
    print(f'\nComparing {labelA} from {fileA} with {labelB} from {fileB}.')
    #input('Press enter for comparison...')
    global exitOK
    boolOK = True
    setA = set(listA).difference(set(listB))
    setB = set(listB).difference(set(listA))

    if len(setA) > 0:
        boolOK=False
        print(os.linesep)
        if fileA == fileB:
            print(f'\n\033[1;31m***{labelA} found in {fileA}, that are not defined as {labelB}!***\033[0;m')
        else:
            print(f'\n\033[1;31m***{labelA} found in {fileA} file, but not in {fileB} file!***\033[0;m')
        pp.pprint(setA)        

    if len(setB) > 0:
        boolOK = False
        print(os.linesep)
        if fileA == fileB:
            print(f'\033[1;31m***{labelB} found in {fileA}, that are not defined as {labelA}!***\033[0;m')
        else:
            print(f'\033[1;31m***{labelB} found in {fileB} file, but not in {fileA} file!***\033[0;m')
        pp.pprint(setB)

    
    if boolOK:
        if labelA == labelB:
            print(f'\033[1;32m{labelA} - OK\033[1;m')
        else:
            print(f'\033[1;32m{labelA} and {labelB} - OK\033[1;m')            

    else:

        exitOK = False

        print('\nFound *'+str(len(listB))+f'* {labelB} in {fileB} file')
        listB.sort()
        pp.pprint(listB)

        print('\nFound *'+str(len(listA))+f'* {labelA} in {fileA} file')
        listA.sort()
        pp.pprint(listA)

    print('\033[0;0m', end='') #reset terminal color. no newline.



if __name__ == '__main__':
    cmdline_args = create_argument_parser().parse_args()
    
    strNluPath = cmdline_args.nlu
    strDomainYmlPath = cmdline_args.domain 
    strStoryPath = cmdline_args.story
    
    #load nlu file
    print("loading NLU file: "+strNluPath)
    with open(strNluPath) as f:
        for line in f:
            #get intents
            if (line.find("## intent:")) > -1:
                nluIntentList.append(line[10:-1])
            #get entities
            if '(' in line:
                nluEntityList.append(line[(line.find('(')+1):(line.find(')'))]) # extract the substring between brackets; line[ opening bracket : closing bracket]

    #remove duplicates from nlu list by hashing
    nluEntityList = list(set(nluEntityList))
    nluEntityList.sort()

    #load story file
    print("loading story file: "+strStoryPath)
    with open(strStoryPath) as f:
        for line in f:
            #get entities
            if '{' in line:
                storyEntityList.append(line[(line.find('{"')+2):(line.find('":'))]) # extract the substring between brackets; line[ opening bracket : closing bracket]


    #remove duplicates from story list by hashing
    storyEntityList = list(set(storyEntityList))
    storyEntityList.sort()


    #load domain file
    print("loading domain file: " + strDomainYmlPath)
    with open(strDomainYmlPath) as stream:
        try:
            loadedDomain= yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            print("with encoding {0}".format(e.encoding))
            print("Invalid char code:", e.character)
            exit("Could not load domain file.")


    #extract data from domain file
    domainIntentList = loadedDomain['intents']
    domainTemplatesList = list(loadedDomain['templates'])  #loadedDomain returns a dict. Assign only the keys. 
    domainTemplatesList.sort()

    domainActionsList = loadedDomain['actions']
    print("Excluding custom actions with . in the name!")
    domainActionsList = [ x for x in domainActionsList if "." not in x ] #remove actions if they contain "." punctuation. This excludes custom actions e.g. ActionSearchLocation. These are not required to be defined as templates.
    domainActionsList.sort()

    domainEntitiesList = loadedDomain['entities']
    domainEntitiesList.sort()

    domainSlotsList = list(loadedDomain['slots'])  #loadedDomain returns a dict. Assign only the keys. 
    domainSlotsList.sort()

    domainTemplatesFull = loadedDomain['templates']
    for valueList in list(domainTemplatesFull.values()): #loadedDomain returns a dict. Assign only the values. 
        #get entities within templates
        for subList in valueList:
            #nested lists within the list of values. Can be string or dict.
            if type(subList) == dict:                
                preprocessList.append(subList["text"])
            else:
                preprocessList.append(subList)

    for element in preprocessList:        
        if '{' in element:
            domainTemplatesSubEntities.append(element[(element.find('{')+1):(element.find('}'))]) # extract the substring between curley brackets; element[ opening-bracket : closing-bracket]    
    #remove duplicate entities by hashing
    domainTemplatesSubEntities = list(set(domainTemplatesSubEntities))
    domainTemplatesSubEntities.sort()

    #compare templates and actions from domain file
    comparison(domainActionsList, domainTemplatesList, "actions", "templates", "domain", "domain")

    #compare intents from nlu file and domain file
    comparison(nluIntentList, domainIntentList, "intents", "intents", "nlu", "domain")

    #compare entities and slots from domain file
    comparison(domainEntitiesList, domainSlotsList, "entities", "slots", "domain", "domain")

    #compare entities from templates and the main of entities within the domain file
    comparison(domainTemplatesSubEntities, domainSlotsList, "entities(templates)", "entities", "domain", "domain")

    #compare entities from stories and the main of entities within the domain file
    comparison(storyEntityList, domainSlotsList, "entities", "entities", "stories", "domain")    

    def yes_or_no(question):
         while "the answer is invalid":
            reply = str(input(question+' (y/n): ')).lower().strip()
            if reply[0] == 'y':
                return True
            if reply[0] == 'n':
                return False

    if exitOK != True:
        if yes_or_no("Inspection found discrepancies. Continue anyway?"): #optional. Use in conjunction with bash script
            exit(0)
        else:
            exit(-1)

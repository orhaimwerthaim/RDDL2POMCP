#This module describes a RDDL domain and instance file.


# Objects:
# Same as RDDL object parameters,
# '':['']- is for fluentes that does not have any parameters
#
# for example:
#  'location': ['$office','$lab','$hallway']
#  'location' is the RDDL domain file 'types' block
#  '$office','$lab','$hallway' are the different location objects as specified in the RDDL 'non-fluents' section in the 'objects' block.
Objects={
    '':[''],
    'robot': ['$armadillo'],
    'location': ['$office','$lab','$hallway'],
    'floor': ['$f1','$f2','$f3'],
    'obj': ['$can']}

#NonFluentDef:
#as specified at the domain file in the 'pvariables' block
# a line in the rddle file:  at_floor(location,floor): {non-fluent, bool, default = false };
# will be translated to:     'at_floor': [('location','floor'),False]
NonFluentDef = {
    'at_floor': [('location','floor'),False]}

#StateFluentsDef:
#as specified at the domain file in the 'pvariables' block
# a line in the rddle file:  object_at(obj,location): {state-fluent, bool, default = false };
# will be translated to:     'object_at': [('obj','robot','location'),False]
StateFluentsDef={
    'object_at': [('obj','robot','location'),False],
    'near': [('robot','location'),False],
    'pickable': [('obj',),False]}

#ActionsDef:
#as specified at the domain file in the 'pvariables' block
# a line in the rddle file:  pick(robot,obj,location): { action-fluent, bool, default = false };
# will be translated to:     'pick':[('robot','obj','location'),False],
ActionsDef={
    'action':[('',),False],
    'pick':[('robot','obj','location'),False],
    'move':[('robot','location','location','floor'),False]}

InitNoneFluent = {
    ('at_floor',('$office','$f2')):True,
    ('at_floor',('$lab','$f2')):True,
    ('at_floor',('$hallway','$f2')):True}

InitState = {('near',('$armadillo','$office')):True,
    ('object_at',('$can','$lab')):True,
    ('pickable',('$can',)):True,
             }

ActionsConstraints = [('robot',1),('obj',1),]

import itertools

def validateActionConstrain(constraint, state):


def updateFluents(fluents, updates):
    for update in updates.items():
        if update[0] in fluents:
            fluents[update[0]]=update[1]

def getGrounded(definitions):
    result = {}
    for definition in definitions.items():
        predicate_objects_lists = []
        for defName in definition[1][0]:
            predicate_objects_lists.append(Objects[defName])

        elements = list(itertools.product(*predicate_objects_lists))
        # elementsWithName = itertools.product([predDef[0]],elements)
        for key in itertools.product([definition[0]], elements):
            result[key] = [definition[1][1]]
    return result

# print('at_floor:')
#for element in itertools.product(Objects['location'],Objects['floor']):
#    print ('at_floor{}' .format(element))

NonFluent = getGrounded(NonFluentDef)
StateFluents = getGrounded(StateFluentsDef)
Actions = getGrounded(ActionsDef)
updateFluents(StateFluents, InitState)
updateFluents(NonFluent, InitNoneFluent)

print('before updating:')

pick=[[key,value] for  key, value in StateFluents.items() if value == True]
print(pick)

updateFluents(StateFluents, InitState)
print('before updating:')

pick=[[key,value] for  key, value in StateFluents.items() if value == True]
print(pick)
# for actDef in ActionsDef.items():
#     action_objects= []
#     for ObjectName in actDef[1][0]:
#         action_objects.append(Objects[ObjectName])
#
#     elements = list(itertools.product(*action_objects))
#     elementsWithValue = itertools.product([actDef[0]], elements, [actDef[1][1]])
#     Actions[actDef[0]] = list(elementsWithValue)

    #for element in elements:
     #   print ('{}{}' .format(predDef[0],element))


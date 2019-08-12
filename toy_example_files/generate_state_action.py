#This module describes a RDDL domain and instance file.

import action_constraint as ac
import itertools

#Objects:
#as specified at the RDDL 'non-fluents' section 'objects' block
# a line in the rddle file:  location : {robot_lab,office,hallway};
# will be translated to:     'location': ['$office','$lab','$hallway'],
Objects={
    '':[''],
    'robot': ['$armadillo'],
    'location': ['$office','$lab','$hallway','$dummy'],
    'floor': ['$f1','$f2','$f3'],
    'obj': ['$can']}

#NonFluentDef:
#as specified at the RDDL domain file in the 'pvariables' block
# a line in the rddle file:  at_floor(location,floor): {non-fluent, bool, default = false };
# will be translated to:     'at_floor': [('location','floor'),False]
NonFluentDef = {
    'at_floor': [('location','floor'),False]}

#StateFluentsDef:
#as specified at the RDDL domain file in the 'pvariables' block
# a line in the rddle file:  object_at(obj,location): {state-fluent, bool, default = false };
# will be translated to:     'object_at': [('obj','robot','location'),False]
StateFluentsDef={
    'object_at': [('obj','robot','location'),False],
    'near': [('robot','location'),False],
    'pickable': [('obj',),False]}

#InitNoneFluent:
#as specified at the RDDL non-fluents section in the 'non-fluents' block
# a line in the rddle file:  at_floor(office,f2);
# will be translated to:     ('at_floor',('$office','$f2')):True,
InitNoneFluent = {
    ('at_floor',('$office','$f2')):True,
    ('at_floor',('$lab','$f2')):True,
    ('at_floor',('$hallway','$f2')):True,
    ('at_floor',('$dummy','$f3')):True}


#InitState:
#as specified at the instance section in the 'init-state' block
# a line in the rddle file:  near(armadillo,office);
# will be translated to:     ('near',('$armadillo','$office')):True,
InitState = {('near',('$armadillo','$office')):True,
    ('object_at',('$can','$lab')):True,
    ('pickable',('$can',)):True,
             }

#ActionsConstraints:
#as specified at the domain file in the 'pvariables' block
# a line in the rddle file:  pick(robot,obj,location): { action-fluent, bool, default = false };
# will be translated to:     'pick':[('robot','obj','location'),False],
#before an action is activated all action-constraints must be true, if not then it is not a legal action
#supported logic operatores are '~','(',')','&','|','>>' (they will be handeled in this order)

#current limitation:
# 1. only one action defined in constraint.
# 2. just the constraints that the action is in can limit it.
# 3. only the action parameters can be in a constraint
ActionsConstraints = [
    [
    ('for_all',(['robot','?r'],['location','?loc'],['location','?dest'],['floor','?f'])),
    ('move',['?r','?loc','?dest','?f']),
    ('>>',),
    ('('),
    ('near',['?r','?loc']),
    ('&'),
    ('at_floor',['?loc','?f']),
    ('&'),
    ('at_floor',['?dest','?f']),
    (')')
    ]
    ]

#ActionsDef:
#as specified at the RDDL domain file in the 'pvariables' block
# a line in the rddle file:  pick(robot,obj,location): { action-fluent, bool, default = false };
# will be translated to:     'pick':[('robot','obj','location'),False],
ActionsDef={
    'action':[('',),False],
    'pick':[('robot','obj','location'),False],
    'move':[('robot','location','location','floor'),False]}




def updateFluents(fluents, updates):
    for update in updates.items():
        if update[0] in fluents:
            fluents[update[0]]=update[1]
            ac.definePredicate(update[0], update[1])

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
            ac.definePredicate(key,definition[1][1])
    return result

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
# print('at_floor:')
#for element in itertools.product(Objects['location'],Objects['floor']):
#    print ('at_floor{}' .format(element))


NonFluent = getGrounded(NonFluentDef)
StateFluents = getGrounded(StateFluentsDef)
Actions = getGrounded(ActionsDef)
updateFluents(StateFluents, InitState)
updateFluents(NonFluent, InitNoneFluent)
print('Fluents')
print(StateFluents)
print('Actions:')
print(Actions)
import datetime
gr_const, notGround = ac.groundContraint(ActionsConstraints[0], ('move', ('$armadillo', '$office', '$lab', '$f2')))
validActio = []
state = merge_two_dicts(NonFluent, StateFluents)
a = datetime.datetime.now()
for key,value in Actions:
    isValid = True
    for const in ActionsConstraints:
        gr_const, notGround = ac.groundContraint(const, (key,value))
        if(len(notGround)>0):#this action is not in the constraint TODO::stop throw exception if action in constrain but constraint is not fully grounded (constraint has parameters not in the action)
            continue
        isValid = ac.validateGroundedConstraint(gr_const, state)
        if not isValid:
            break
    if isValid:
        validActio.append((key,value))
b = datetime.datetime.now()
c = b - a
print('c.seconds:{}' .format(c.seconds))
print('c.microseconds:{}' .format(c.microseconds))
print('valid actions:')
print (validActio)


#print(ActionsConstraints)
# print('before updating:')
#
# pick=[[key,value] for  key, value in StateFluents.items() if value == True]
# print(pick)
#
# updateFluents(StateFluents, InitState)
# print('before updating:')
#
# pick=[[key,value] for  key, value in StateFluents.items() if value == True]
# print(pick)
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


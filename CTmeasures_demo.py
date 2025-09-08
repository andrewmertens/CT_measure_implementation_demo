from __future__ import division
import random, glob, time, os
from math import sqrt
from psychopy import core, visual, event, gui

### Get parameters and setup stimuli
myWin = visual.Window(units='norm', fullscr=True, color='grey', monitor='testMonitor')
windowSize = myWin.size
myMouse = event.Mouse()
myClock = core.Clock()
doneBox = visual.Rect(myWin, width=.15, height=.1, pos=(.8, -.85), fillColor="white", lineColor="black")
doneText = visual.TextStim(myWin, text="Done", pos=(.8, -.85), color='black', height=.1)
doneHighlight = visual.Rect(myWin, width=.15, height=.1, pos=(.8, -.85), lineWidth=5, lineColor="blue")
Welcome = visual.TextStim(myWin, text='Hello! Press the space bar to start.', color='white')
BD_expl = visual.TextStim(myWin, text='The following screen will demonstrate a trial modeled from the WISC-III Block Design task. The program is set up to record accuracy but this demo version does not store that data. Press the spacebar to proceed.', color='white')
RP_expl = visual.TextStim(myWin, text='The following screen will demonstrate a trial modeled from the Leiter-R Repeated Patterns task. The program is set up to record accuracy but this demo version does not store that data. Press the spacebar to proceed.', color='white')
ThankYou = visual.TextStim(myWin, text='Thank you for viewing this demo. Press the spacebar to end.', color='white')

#---
Welcome.draw()
myWin.flip()
keys = event.waitKeys(keyList=['space','escape'])
if keys[0] == 'escape': core.quit()
#---

###Block Design:

##Stimuli and variables:

#set block size based on monitor
blockW=.19
blockH=(blockW*windowSize[0])/windowSize[1]

#setup stimuli
myBlocks = []
myBlocks.append(visual.ImageStim(myWin, image='stim/blocks/smiley2_1.png', size=(blockW,blockH), pos=(-.45, -.5)))
myBlocks.append(visual.ImageStim(myWin, image='stim/blocks/smiley1_2.png', size=(blockW,blockH), pos=(-.15, -.5)))
myBlocks.append(visual.ImageStim(myWin, image='stim/blocks/smiley2_2.png', size=(blockW,blockH), pos=(.15, -.5)))
myBlocks.append(visual.ImageStim(myWin, image='stim/blocks/smiley1_1.png', size=(blockW,blockH), pos=(.45, -.5)))

BDdemoItem = visual.ImageStim(myWin, image='stim/BD_items/smiley.png', size=(blockW*2,blockH*2), pos=(-.2-(blockW/2), .6-(blockH/2)))

#setup grid spaces to place blocks
myGridBoxes = []
myGridBoxes.append(visual.Rect(myWin, width=blockW, height=blockH, pos=(.2,.6), lineWidth=5, lineColor='black')) #top-left
myGridBoxes.append(visual.Rect(myWin, width=blockW, height=blockH, pos=(.2+blockW,.6), lineWidth=5, lineColor='black')) #top-middle
myGridBoxes.append(visual.Rect(myWin, width=blockW, height=blockH, pos=(.2,.6-blockH), lineWidth=5, lineColor='black')) #middle-left
myGridBoxes.append(visual.Rect(myWin, width=blockW, height=blockH, pos=(.2+blockW,.6-blockH), lineWidth=5, lineColor='black')) #middle-middle

grid1 = myGridBoxes[0]
grid2 = myGridBoxes[1]
grid3 = myGridBoxes[2]
grid4 = myGridBoxes[3]

myGridBoxImages = []
myGridBoxImages.append(visual.ImageStim(myWin, image=None, size=(blockW,blockH), pos=grid1.pos))
myGridBoxImages.append(visual.ImageStim(myWin, image=None, size=(blockW,blockH), pos=grid2.pos))
myGridBoxImages.append(visual.ImageStim(myWin, image=None, size=(blockW,blockH), pos=grid3.pos))
myGridBoxImages.append(visual.ImageStim(myWin, image=None, size=(blockW,blockH), pos=grid4.pos))

myGrid = [myGridBoxes[0:4]] #adapted from full version with multiple trials where number of grid boxes is variable
myGridImages = [myGridBoxImages[0:4]]

#setup interaction highlighting
blockHighlightBlue = visual.Rect(myWin, width=blockW, height=blockH, pos=(0,0), lineWidth=8, lineColor='blue')
blockHighlightBlue2 = visual.Rect(myWin, width=blockW, height=blockH, pos=(0,0), lineWidth=8, lineColor='blue')
blockHighlight = visual.Rect(myWin, width=blockW, height=blockH, pos=(0,0), lineWidth=8, lineColor='yellow')

#setup target (correct) response, for scoring
DemoTargets = []
DemoTargets.append('stim/blocks/smiley1_1.jpg')
DemoTargets.append('stim/blocks/smiley1_2.jpg')
DemoTargets.append('stim/blocks/smiley2_1.jpg')
DemoTargets.append('stim/blocks/smiley2_2.jpg')

myTargets = [[DemoTargets]]

#Explain demo trial
BD_expl.draw()
myWin.flip()
keys = event.waitKeys(keyList=['space','escape'])
if keys[0] == 'escape': core.quit()

##Trial (in full version this code would be looped through multiple trials)
firstBlockClicked=False
blockSelected=False
done=False
BDdemoItem.draw()
#Draw starting stimuli
for block in myBlocks:
    block.draw()
for grid in myGrid[0]:
    grid.draw()
for gridImage in myGridImages[0]:
    gridImage.image=None
myWin.flip()
myClock.reset()
while not firstBlockClicked:
    #wait for first click
    while not myMouse.getPressed()[0]:
        keys=event.getKeys()
        if 'escape' in keys: core.quit()
    clickLocation=myMouse.getPos()
    #if click is in one of the blocks, highlight it
    for index,block in enumerate(myBlocks):
        if block.contains(clickLocation):
            blockSelected=True
            blockHighlight.pos=block.pos
            selectedBlockIndex=index
            firstBlockClicked=True
        else:
            continue
    while myMouse.getPressed()[0]:
        continue
#redraw stimuli including block highlight
BDdemoItem.draw()
for block in myBlocks:
    block.draw()
for grid in myGrid[0]:
    grid.draw()
for gridImage in myGridImages[0]:
    gridImage.image=None
blockHighlight.draw()
doneBox.draw()
doneText.draw()
myWin.flip()
#until 'done' button is pressed...
while not done:
    while not myMouse.getPressed()[0]:
        keys=event.getKeys()
        if 'escape' in keys: core.quit()
    clickLocation=myMouse.getPos()
    #if 'done' button is clicked, set param to end trial
    if doneBox.contains(clickLocation):
        rt=myClock.getTime()
        done=True
    #if a block is clicked, set param to highlight it
    for index,block in enumerate(myBlocks):
        if block.contains(clickLocation):
            blockSelected=True
            blockHighlight.pos=block.pos
            selectedBlockIndex=index
    #is a grid space is clicked while a block is selected, change the grid image to that of the block's image
    for index,grid in enumerate(myGrid[0]):
        if grid.contains(clickLocation) and blockSelected:
            myGridImages[0][index].image=myBlocks[selectedBlockIndex].image
    #update screen
    BDdemoItem.draw()
    for block in myBlocks:
        block.draw()
    for grid in myGrid[0]:
        grid.draw()
    for gridImages in myGridImages[0]:
        gridImages.draw()
    if blockSelected: blockHighlight.draw()
    doneBox.draw()
    doneText.draw()
    myWin.flip()
    while myMouse.getPressed()[0]:
        continue
#check if ending grid matches target pattern and score accuracy
for index, target in enumerate(myTargets[0]):
    if target == myGridImages[0][index].image:
        acc=1
    else: acc=0
myWin.flip()



### Repeated Patterns

#Explain demo trial
RP_expl.draw()
myWin.flip()
keys = event.waitKeys(keyList=['space','escape'])
if keys[0] == 'escape': core.quit()

##Stimuli and variables:
#set tile size based on monitor
cardW = .275
cardH = (cardW*windowSize[0])/windowSize[1]

#setup stimuli
RPdemoItems = []
RPdemoItems.append(visual.ImageStim(myWin, image='stim/RP_items/A.png', size=(cardW,cardH), pos=(-.8625,.5)))
RPdemoItems.append(visual.ImageStim(myWin, image='stim/RP_items/B.png', size=(cardW,cardH), pos=(-.575,.5)))
RPdemoItems.append(visual.ImageStim(myWin, image='stim/RP_items/A.png', size=(cardW,cardH), pos=(-.2875,.5)))
RPdemoItems.append(visual.ImageStim(myWin, image='stim/RP_items/B.png', size=(cardW,cardH), pos=(0,.5)))
RPdemoItems.append(visual.ImageStim(myWin, image='stim/RP_items/A.png', size=(cardW,cardH), pos=(.2875,.5)))

#setup interactive cards
RPdemoCards = []
RPdemoCards.append(visual.ImageStim(myWin, image='stim/RPcards/C.png', size=(cardW,cardH), pos=(-.5,-.5)))
RPdemoCards.append(visual.ImageStim(myWin, image='stim/RPcards/B.png', size=(cardW,cardH), pos=(0,-.5)))
RPdemoCards.append(visual.ImageStim(myWin, image='stim/RPcards/A.png', size=(cardW,cardH), pos=(.5,-.5)))

#steup slots for interactive cards to be placed
demoCardSlots = []
demoCardSlots.append(visual.Rect(myWin, width=cardW, height=cardH, pos=(.575,.5), lineWidth=5, lineColor='black'))
demoCardSlots.append(visual.Rect(myWin, width=cardW, height=cardH, pos=(.8625,.5),lineWidth=5, lineColor='black'))
demoCardSlotImages = []
demoCardSlotImages.append(visual.ImageStim(myWin, image=None, size=(cardW,cardH), pos=(.575,.5)))
demoCardSlotImages.append(visual.ImageStim(myWin, image=None, size=(cardW,cardH), pos=(.8625,.5)))

#setup target response
RPsampleTargets = []
RPsampleTargets.append('stim/RPcards/B.png')
RPsampleTargets.append('stim/RPcards/A.png')

RPitems = [RPdemoItems]

#setup done button
RPdoneBox = visual.Rect(myWin, width=.15, height=.1, pos=(.8, -.9), fillColor="white", lineColor="black")
RPdoneText = visual.TextStim(myWin, text="Done", pos=RPdoneBox.pos, color='black', height=.1)

#setup interaction highlighting
RPdoneHighlight = visual.Rect(myWin, width=.15, height=.1, pos=RPdoneBox.pos, lineWidth=8, lineColor='blue')
RPhighlight = visual.Rect(myWin, width=cardW, height=cardH, lineWidth=8, lineColor='yellow') #use with itemIndex

startingVertCardPos = -.5

##Trials (in full version this code would be looped through multiple trials)
#draw starting stimuli
for i in RPdemoItems:
    i.draw()
for slot in demoCardSlots:
    slot.draw()
for card in RPdemoCards:
    card.draw()
#initialize parameters
firstCardClicked=False
selectedSlotIndex=None
selectedCardIndex=None
slotSelected=False #Not redundant with slotClicked/cardClicked
cardSelected=False
done=False
myClock.reset()
myWin.flip()
#wait for first click
while not firstCardClicked:
    while not myMouse.getPressed()[0]:
        keys=event.getKeys()
        if 'escape' in keys: core.quit()
    clickLocation=myMouse.getPos()
    #if first click is on an card, mark it as selected and highlight 
    for index,card in enumerate(RPdemoCards):
        if card.contains(clickLocation):
            RPhighlight.pos=card.pos
            cardClicked=True
            selectedCardIndex=index
            slotSelected=False
            cardSelected=True
            firstCardClicked=True
        else:
            continue
    while myMouse.getPressed()[0]:
        continue
#redraw screen
for i in RPdemoItems:
    i.draw()
for slot in demoCardSlots:
    slot.draw()
for card in RPdemoCards:
    card.draw()
RPhighlight.draw()
RPdoneBox.draw()
RPdoneText.draw()
myWin.flip()
#until 'done' button is pressed...
while not done:
    while not myMouse.getPressed()[0]:
        keys=event.getKeys()
        if 'escape' in keys: core.quit()
    clickLocation=myMouse.getPos()
    cardClicked=False
    slotClicked=False
    #check to see if a visible card is clicked
    for card in RPdemoCards:
        if card.contains(clickLocation):
            if card.opacity==0:
                continue
            cardClicked=True
    #check to see if a card slot is clicked
    for slot in demoCardSlots:
        if slot.contains(clickLocation):
            slotClicked=True
    #when card is selected and a valid slot is clicked, changes the image in the previously clicked slot invisible (before updating slot index)
    for index,slot in enumerate(demoCardSlots):
        if selectedSlotIndex is not None and selectedCardIndex is not None and slot.contains(clickLocation) and demoCardSlotImages[selectedSlotIndex].image==RPdemoCards[selectedCardIndex].image:
            demoCardSlotImages[selectedSlotIndex].image=None
    #change the highlight and selection index if a new card is clicked
    for index,card in enumerate(RPdemoCards):
        if card.contains(clickLocation) and card.pos[1]==startingVertCardPos and card.opacity==1:
            RPhighlight.pos=card.pos
            selectedCardIndex=index
            slotSelected=False
            cardSelected=True
    #change the selection index if a new slot is clicked
    for index,slot in enumerate(demoCardSlots):
        if slot.contains(clickLocation):
            selectedSlotIndex=index 
            slotSelected=True
    #makes the card reappear in its starting position if another card replaces it in a slot
    for index,card in enumerate(RPdemoCards):
        if slotSelected and card.image==demoCardSlotImages[selectedSlotIndex].image:
            card.opacity=1
            slotSelected=False
    for index,slot in enumerate(demoCardSlots):
        if slot.contains(clickLocation) and cardSelected:
            RPdemoCards[selectedCardIndex].opacity=0 
            demoCardSlotImages[index].image=RPdemoCards[selectedCardIndex].image
            demoCardSlotImages[index].opacity=1 #makes a card disappear from its starting position and appear in the selected slot
            RPhighlight.pos=slot.pos #also reassigns the highlight to the slot's position to show the card is still selected
    #redraw screen
    for i in RPdemoItems:
        i.draw()
    for slotImages in demoCardSlotImages:
        slotImages.draw()
    for slot in demoCardSlots:
        slot.draw()
    for card in RPdemoCards:
        card.draw()
    RPhighlight.draw()
    RPdoneBox.draw()
    RPdoneText.draw()
    myWin.flip()
    #check to see if done button is pressed. If it is, end trial
    if RPdoneBox.contains(clickLocation):
        rt=myClock.getTime()
        done=True
    elif not cardClicked and not slotClicked:
        continue #returns to the top of the loop if nothing "clickable" is clicked
    while myMouse.getPressed()[0]:
        continue
for index,target in enumerate(RPsampleTargets):
    if demoCardSlotImages[index].image == target:
        RPacc=1
    else:
        RPacc=0

#---
ThankYou.draw()
myWin.flip()
#---

keys = event.waitKeys(keyList=['space','escape'])
if keys[0] == 'escape': core.quit()
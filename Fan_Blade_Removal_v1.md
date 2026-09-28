## SOP-00: Introduction

**SOP Gate** 
- Unlock condition: Start of sim 
- Completion flag: `Flag_SOP00_Step02_Introduction` 

**Tasks used in this SOP** 
- `PressOkToContinue` 

### Step 00.1: Present goal

**Trigger:** SOP-00 becomes active 

**System UI** 
- **Title**: "Fan Blade Removal Training Sim" 
- **Body**: "Press Start to Begin." 
- Button: **Start** 

**Tasks** 
- `PressOkToContinue` → sets `Flag_SOP00_Step01_PressStart` 

**Advance when:** `Flag_SOP00_Step01_PressStart == true`   

### Step 00.2: Present goal

**Trigger:** `Flag_SOP00_Step01_PressStart == true` 

**System UI** 
- **Title**: "Fan Blade Removal Training Sim" 
- **Body**: "This tutorial walks you through a simplified fan blade removal and installation process on the GE MX engine.
Fan blades and platforms are balance-critical. If you're reinstalling the same components, they must go back in their original positions.
To ensure correct sequencing, each blade and platform should be numbered before removal." 
- Button: **OK** 

**Tasks** 
- `PressOkToContinue` → sets `Flag_SOP00_Step02_Introduction` 

**Advance when:** `Flag_SOP00_Step02_Introduction == true`   

## SOP-01: Index the fan and label all blades/platforms (1-18) 

**SOP Gate** 
- Unlock condition: `Flag_SOP00_Step02_Introduction == true` 
- Completion flag: `Flag_SOP01_Labeled` 
  
**Tasks used in this SOP** 
- `PressOkToContinue` 
- `RotateAssemblyToAlignment(targetId, targetClock)` 
- `ApplyLabel(targetId, labelId)`

### Step 01.1: Present goal

**Trigger:** `Flag_SOP00_Introduction == true`

**System UI** 
- **Title**: "SOP-01: Identify Blade #1" 
- **Body**: "First, we’ll find the reference position used for balancing and labeling.

Because of the fan’s size, we’ll lower it into the ground for this demo.

Press OK to continue." 
- Button: **OK** 

**Tasks** 
- `PressOkToContinue` → sets `Flag_SOP01_Step01_AckGoal` 

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`others`</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`PF_EngineFanAssembly`</td>
      <td>Yes</td>
      <td>Visible, but locked interaction until OK</td>
    </tr>
    <tr>
      <td>`PF_Spinner`</td>
      <td>Yes</td>
      <td>Dimple must be visible</td>
    </tr>
    <tr>
      <td>`PF_FanBlade_01..18`</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>`PF_Platform_01..18`</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>`PF_WorkTable`</td>
      <td>Yes</td>
      <td>Behind user</td>
    </tr>
    <tr>
      <td>`PF_ServiceTrolley`</td>
      <td>Yes</td>
      <td>Behind user</td>
    </tr>
    <tr>
      <td>`PF_Tool_CrankBar`</td>
      <td>Yes</td>
      <td>Present but non-interactable</td>
    </tr>
    <tr>
      <td>`others`</td>
      <td>Yes</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP01_Step01_AckGoal == true`   

### Step 01.2: Prompt rotation to locate Blade #1

**Trigger:** `Flag_SOP01_Step01_AckGoal == true`   

**System UI**    
- **Body**: "Rotate the fan until the spinner dimple is at the top; which is the 12 o’clock position."   
        
**Tasks**           
- `RotateAssemblyToAlignment(target="SpinnerDimple", targetClock="12")`           
  - Sets: `Flag_SOP01_DimpleAt12`           

**Interactable**           
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_EngineFanAssembly</td>
      <td>Yes</td>
      <td>Rotation enabled (snap tolerance recommended)</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Optional</td>
      <td>If you want blade-grab rotation</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Advance when:** Flag_SOP01_DimpleAt12 == true   

### Step 01.3: Acknowledge + auto-label

**Trigger:** `Flag_SOP01_DimpleAt12 == true`

**System UI**
- **Body**: "Nice work! The spinner dimple points to balance position one.

Next, we’ll label all blades and platforms counterclockwise.

We’ll handle that for you. Press OK to continue."

**Tasks**
- Apply labels using `ApplyLabel(targetId, labelId)` in a loop for blades 1 to 18
- Apply labels using `ApplyLabel(targetId, labelId)` in a loop for platforms 1 to 18
  - Sets: `Flag_SOP01_LabelsVisible`
- `PressOkToContinue` → sets `Flag_SOP01_Labeled`
**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active** 
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Yes</td>
      <td>Labels become visible</td>
    </tr>
    <tr>
      <td>PF_Platform_01..18</td>
      <td>Yes</td>
      <td>Labels become visible</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP01_Labeled == true`

## SOP-02: Remove spinner bolts (18)      
**SOP Gate**      
- Unlock condition: `Flag_SOP01_Labeled == true`      
- Completion flag: `Flag_SOP02_SpinnerBoltsRemoved`     
**Tasks used in this SOP**      
- `PressOkToContinue`      
- `RemoveBolt(boltGroupId)`      

### Step 02.1: Present goal

**Trigger:** `SOP-02 becomes active`

**System UI**
- **Title**: "SOP-02: Loosen a spinner bolt"
- **Body**: "Now, we’ll loosen the spinner bolts.

Place the screwdriver onto the spinner bolt of fan blade #1, then turn counter-clockwise to loosen it. You can find the screwdriver on the work table behind you.

**Tasks**
- `RemoveBolt(boltGroupId="PF_BoltGroup_Spinner")` 
  - sets `Flag_SOP02_OneSpinnerBoltRemoved`
  - 
**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_Tool_CrankBar</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_BoltGroup_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP02_OneSpinnerBoltRemoved == true`

### Step 02.3: Acknowledge completion

**Trigger:** `Flag_SOP02_OneSpinnerBoltRemoved == true`

**System UI**
- **Body**: "Great! We’ll take care of the remaining bolts. Press OK to continue."
- Button: **OK**

**Tasks**
- `PressOkToContinue` → sets `Flag_SOP02_SpinnerBoltsRemovedAck`
- **Notes**: System action after OK marks the remaining spinner bolts as removed
  - Sets: `Flag_SOP02_SpinnerBoltsRemoved`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_Tool_CrankBar</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_BoltGroup_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP02_SpinnerBoltsRemovedAck == true`

## SOP-03: Remove the spinner and place it on the table           
**SOP Gate**           
- Unlock condition: `Flag_SOP02_SpinnerBoltsRemovedAck == true`           
- Completion flag: `Flag_SOP03_SpinnerStowed`     
       
**Tasks used in this SOP**           
- `PressOkToContinue`           
- `DetachPart(partId)`        
- `PlacePartInZone(partId, zoneId)`           


### Step 03.1: Prompt removal

**Trigger:** `SOP-03 becomes active`

**System UI**
- **Title**: "SOP-03: Remove Spinner"
- **Body**: "Now we'll remove the spinner and place it on the work table. Support the spinner with both hands, and remove it. 

Reminder: We removed the remaining bolts for you in the previous SOP. In a real scenario, you have to make sure that you hold the weight of the spinner when you remove the last bolts. "

**Tasks**
- `DetachPart(partId="PF_Spinner")`
  - sets `Flag_SOP03_SpinnerDetached`
  - 
**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_Tool_CrankBar</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_BoltGroup_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP03_SpinnerDetached == true`

### Step 03.3: Place the spinner on the table

**Trigger:** `Flag_SOP03_SpinnerDetached == true`

**System UI**
- **Body**: "Great! Now, place the spinner on the work table."

**Tasks**
- `PlacePartInZone(partId="PF_Spinner", zoneId="Zone_Table_Spinner")`
  - sets `Flag_SOP03_SpinnerStowed`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP03_SpinnerStowed == true`

## SOP-04: Remove support ring bolts (18), remove support ring, place on table      
**SOP Gate**      
- Unlock condition: `Flag_SOP03_SpinnerStowed == true`      
- Completion flag: `Flag_SOP04_SupportRingStowed`     
  
**Tasks used in this SOP**      
- `PressOkToContinue`      
- `RemoveBolt(boltGroupId)`      
- `DetachPart(partId)`      
- `PlacePartInZone(partId, zoneId)`      

### Step 04.1: Present goal

**Trigger:** `SOP-04 becomes active`

**System UI**
- **Title**: "Task 4: Remove Support Ring"
- **Body**: "Now, we'll remove 22 support ring bolts. 
Place the screwdriver onto the support ring bolt of fan blade #1, then turn counter-clockwise to loosen it."

**Tasks**
- `RemoveBolt(boltGroupId="PF_BoltGroup_SupportRing")`  
  - sets `Flag_SOP04_OneSupportRingBoltRemoved`

**Advance when:** `Flag_SOP04_OneSupportRingBoltRemoved == true`

### Step 04.3: Acknowledge + detach ring

**Trigger:** `Flag_SOP04_OneSupportRingBoltRemoved == true`

**System UI**
- **Body**: "Great! We'll take the rest off for you. Press OK to continue."

**Tasks**
- System action on enter marks the remaining support ring bolts as removed  
  - sets `Flag_SOP04_SupportRingBoltsRemoved`
- `DetachPart(partId="PF_SupportRing")` 
  - sets `Flag_SOP04_SupportRingDetached`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP04_SupportRingDetached == true`

### Step 04.4: Place the ring on the table

**Trigger:** `Flag_SOP04_SupportRingDetached == true`

**System UI**
- **Body**: "The support ring is now free. Please lift it off carefully with both hands and place it on the work table."

**Tasks**
- `PlacePartInZone(partId="PF_SupportRing", zoneId="Zone_Table_SupportRing")` 
  - sets `Flag_SOP04_SupportRingStowed`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
      <td>On table in SPINNER area</td>
    </tr>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
      <td>While placing, then on table in SUPPORT RING area</td>
    </tr>
    <tr>
      <td>PF_EngineFanAssembly</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Platform_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
      <td>Behind user</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP04_SupportRingStowed == true`

## SOP-05: Index Blade #8 to 6 o'clock      
**SOP Gate**      
- Unlock condition: `Flag_SOP04_SupportRingStowed == true`      
- Completion flag: `Flag_SOP05_Blade08Indexed`      

**Tasks used in this SOP**      
- `PressOkToContinue`      
- `RotateAssemblyToAlignment(targetId, targetClock)`      

### Step 05.1: Present goal

**Trigger:** `SOP-05 becomes active`

**System UI**
- **Title**: "Task 5: Align Blade #8"
- **Body**: "Good job! Now, rotate the fan counterclockwise until Blade #8 is at the 6 o'clock position. "

**Tasks**
- `RotateAssemblyToAlignment(target="Blade08", targetClock="6")` 
  - sets `Flag_SOP05_Blade08At6`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
      <td>On table in SPINNER area</td>
    </tr>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
      <td>While placing, then on table in SUPPORT RING area</td>
    </tr>
    <tr>
      <td>PF_EngineFanAssembly</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Platform_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
      <td>Behind user</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP05_Blade08At6 == true`

### Step 05.3: Completion confirmation

**Trigger:** `Flag_SOP05_Blade08At6 == true`

**System UI**
- **Body**: "Nice work! Blade #8 is aligned at 6 o'clock. Press OK to continue."
- Button: **OK**

**Tasks**
- `PressOkToContinue` → sets `Flag_SOP05_Blade08Indexed`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP05_Blade08Indexed == true`

## SOP-06: Remove Platform #8 and stow on the table           
**SOP Gate**           
- Unlock condition: `Flag_SOP05_Blade08Indexed == true`           
- Completion flag: `Flag_SOP06_Platform08Stowed`     
      
**Tasks used in this SOP**           
- `PressOkToContinue`           
- `DetachPart(partId="PF_Platform_08")`           
- `PlacePartInZone(partId="PF_Platform_08", zoneId="Zone_Table_Platform")`

### Step 06.1: Present goal

**Trigger:** `SOP-06 becomes active`

**System UI**
- **Title**: "Task 6: Remove Platform #8"
- **Body**: "Now, we'll remove Platform #8 carefully and place it on the work table. Pull it straight out. Be cautious not to scrap or rub against the blades."

**Tasks**
- `DetachPart(partId="PF_Platform_08")` → sets `Flag_SOP06_PlatformDetached`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_EngineFanAssembly</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Platform_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
      <td>On table in SPINNER area</td>
    </tr>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
      <td>While placing, then on table in SUPPORT RING area</td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
      <td>Behind user</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP06_PlatformDetached == true`

### Step 06.3: Place the platform on the table

**Trigger:** `Flag_SOP06_PlatformDetached == true`

**System UI**
- **Body**: "Place Platform #8 on the work table in the PLATFORM area."

**Tasks**
- `PlacePartInZone(partId="PF_Platform_08", zoneId="Zone_Table_Platform")` 
  - sets `Flag_SOP06_Platform08Placed`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_Platform_08</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP06_Platform08Placed == true`

### Step 06.4: Completion confirmation

**Trigger:** `Flag_SOP06_Platform08Placed == true`

**System UI**
- **Body**: "Great! Platform #8 is stowed on the work table. Press OK to continue."
- Button: **OK**

**Tasks**
- `PressOkToContinue` → sets `Flag_SOP06_Platform08Stowed`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP06_Platform08Stowed == true`

## SOP-07: Remove Fan Blade #8 and send to service trolley      
**SOP Gate**      
- Unlock condition: `Flag_SOP06_Platform08Stowed == true`      
- Completion flag: `Flag_SOP07_Blade08SentToService`   
   
**Tasks used in this SOP**      
- `PressOkToContinue`      
- `DetachPart(partId="PF_FanBlade_08")`      
- `PlacePartInZone(partId="PF_FanBlade_08", zoneId="Zone_Trolley_Blade")`      
- `ApplyLabel(targetId="PF_FanBlade_08", labelId="Fan blade 8")`     

### Step 07.1: Present goal

**Trigger:** `SOP-07 becomes active`

**System UI**
- **Title**: "Task 7: Remove Fan Blade #8"
- **Body**: "We raised up the fan assembly for the remaining steps. 
Now, we'll remove Fan Blade #8. Pull it gently outward from the assembly."

**Tasks**
- `DetachPart(partId="PF_FanBlade_08")` → sets `Flag_SOP07_BladeDetached`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_EngineFanAssembly</td>
      <td>Yes</td>
      <td>Visible, but locked interaction until OK</td>
    </tr>
    <tr>
      <td>PF_FanBlade_01..18</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Platform_01..18</td>
      <td>Yes</td>
      <td>(Platform #8 removed)</td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_WorkTable</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_Spinner</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>PF_SupportRing</td>
      <td>Yes</td>
      <td></td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP07_BladeDetached == true`

### Step 07.3: Place the blade on the trolley

**Trigger:** `Flag_SOP07_BladeDetached == true`


**System UI**
- **Body**: "Awesome! Place Fan Blade #8 on the service trolley."

**Tasks**
- `PlacePartInZone(partId="PF_FanBlade_08", zoneId="Zone_Trolley_Blade")` → sets `Flag_SOP07_BladePlacedOnTrolley`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_FanBlade_08</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP07_BladePlacedOnTrolley == true`

### Step 07.4: Label confirmation


**Trigger:** `Flag_SOP07_BladePlacedOnTrolley == true`


**System UI**
- **Body**: "We will now label the blade '#8' to preserve balance tracking."

**Tasks**
- `ApplyLabel(targetId="PF_FanBlade_08", labelId="Fan blade 8")` → sets `Flag_SOP07_Blade08Labeled`

**Interactable**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Interactable?</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_FanBlade_08</td>
      <td>Yes</td>
      <td>Label attaches to blade</td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Optional</td>
      <td>If represented as a prop or UI driven sticker</td>
    </tr>
    <tr>
      <td>others</td>
      <td>No</td>
      <td></td>
    </tr>
  </tbody>
</table>

**Active**
<table>
  <thead>
    <tr>
      <th>Prefab</th>
      <th>Active?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PF_FanBlade_08</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>PF_ServiceTrolley</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>others</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

**Advance when:** `Flag_SOP07_Blade08Labeled == true`

### Step 07.5: Completion confirmation


**Trigger:** `Flag_SOP07_Blade08Labeled == true`


**System UI**
- **Body**: "Excellent. Fan Blade #8 is on the trolley and labelled for service. Congratulations, you have finished the Fan Blade Removal Training Simulation."
- Button: **Finish**

**Tasks**
- `PressOkToContinue` → sets `Flag_SOP07_Blade08SentToService`

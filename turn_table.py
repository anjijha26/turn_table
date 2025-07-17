import maya.cmds as cmds
import math


def turnTable_GUI():
    # Clean up previous window if it exists
    if cmds.window("TurnTableWin", exists=True):
        cmds.deleteUI("TurnTableWin")

    winName = cmds.window("TurnTableWin", title="Turn Table")
    cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 10), (2, 160), (3, 10), (4, 160), (5, 10)])

    # Start Time
    cmds.separator(h=10, style='none')
    cmds.text(label="Start Time")
    cmds.separator(h=10, style='none')
    start_field = cmds.intField("start", min=1, value=1)
    cmds.separator(h=10, style='none')

    # Spacer
    [cmds.separator(h=10) for _ in range(5)]

    # End Time
    cmds.separator(h=10, style='none')
    cmds.text(label="End Time")
    cmds.separator(h=10, style='none')
    end_field = cmds.intField("end", value=40)
    cmds.separator(h=10, style='none')

    # Spacer
    [cmds.separator(h=10) for _ in range(5)]

    # Lighting and Floor Checkboxes
    cmds.separator(h=10, style='none')
    cmds.checkBox("creatingLight", label='Create Lighting')
    cmds.separator(h=10, style='none')
    cmds.checkBox("creatingFloor", label='Create Floor')
    cmds.separator(h=10, style='none')

    # Spacer
    [cmds.separator(h=10) for _ in range(5)]

    # Camera Rotation Direction
    cmds.separator(h=10, style='none')
    cmds.text(label="Direction of Camera Rotation:")
    cmds.radioCollection("camDirection")
    cmds.separator(h=10, style='none')
    cmds.radioButton('clockwise', label='Clockwise', select=True)
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.radioButton('counterClockwise', label='Counter-Clockwise')
    cmds.separator(h=10, style='none')

    # Spacer
    [cmds.separator(h=10) for _ in range(5)]

    # Camera Radius
    cmds.separator(h=10, style='none')
    cmds.text(label="Radius of Pivot: ")
    cmds.separator(h=10, style='none')
    cmds.intSliderGrp("cameraRadius", field=True, minValue=20, maxValue=80, value=20)
    cmds.separator(h=10, style='none')

    # Spacer
    [cmds.separator(h=10) for _ in range(5)]

    # Buttons
    cmds.separator(h=10, style='none')
    cmds.button(label='Close Window', command=('cmds.deleteUI(\"' + winName + '\", window=True)'))
    cmds.separator(h=10, style='none')
    cmds.button(label="Create Turntable", command="createTurntable()")
    cmds.separator(h=10, style='none')

    # Final Spacer
    [cmds.separator(h=10, style='none') for _ in range(5)]

    cmds.showWindow(winName)


def createTurntable():
    try:
        start = cmds.intField('start', q=True, v=True)
        end = cmds.intField('end', q=True, v=True)
        creatingLight = cmds.checkBox('creatingLight', q=True, v=True)
        creatingFloor = cmds.checkBox('creatingFloor', q=True, v=True)
        camRadius = cmds.intSliderGrp('cameraRadius', q=True, v=True)
        camDirection = cmds.radioCollection("camDirection", q=True, select=True)

        # Create Lights
        if creatingLight:
            for name, pos, rot, intensity in [
                ('KeyLight', (12, 10, -12), (-25, 130, 0), 3.5),
                ('FillLight', (-12, 10, -12), (-25, -130, 0), 0.8),
                ('BackLight', (-12, 10, 12), (-25, -45, 0), 2.0),
            ]:
                if cmds.objExists(name):
                    cmds.delete(name)
                light = cmds.directionalLight(n=name, intensity=intensity)
                light_transform = cmds.listRelatives(light, parent=True)[0]
                cmds.xform(light_transform, translation=pos, rotation=rot)
                print(f"{name} Created")
            cmds.group('KeyLight', 'FillLight', 'BackLight', n="TurnTableLights")
            print("TurnTableLights Group Created")
        else:
            print("Lights not created, option not selected")

        # Create Floor
        if creatingFloor:
            if cmds.objExists('TurnTableFloor'):
                cmds.delete('TurnTableFloor')
            cmds.polyPlane(n='TurnTableFloor', h=24, w=24)
            print("Floor Created")
        else:
            print("Floor not created, option not selected")

        # Create Camera on Motion Path
        radius = camRadius
        path = cmds.circle(n='MotionPath', nr=(0, 1, 0), c=(0, 0, 0), r=radius)[0]
        follower = cmds.spaceLocator(n="Follower")[0]
        focus = cmds.spaceLocator(n="CameraAim")[0]
        cam = cmds.camera(n="ShotCam")[0]
        cmds.group(path, follower, focus, cam, n="MotionPathCameraSetup")
        cmds.parent(cam, follower)
        cmds.aimConstraint(focus, cam, offset=(0, -90, 0))

        # Ensure correct motion path direction
        if camDirection == 'counterClockwise':
            cmds.setAttr(path + ".scaleX", -1)  # Reverse path direction

        cmds.pathAnimation(follower, path, startTimeU=start, endTimeU=end)
        print(
            f"Turntable Camera Created - {'Counter-Clockwise' if camDirection == 'counterClockwise' else 'Clockwise'}")

    except Exception as e:
        cmds.warning(f"Failed to create turntable: {e}")


# Run the GUI
turnTable_GUI()

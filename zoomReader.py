#pyobjc packages
from AppKit import NSWorkspace#type: ignore
#ApplicationServices for accessibility APIs (to access zoom desktop app)
from ApplicationServices import AXIsProcessTrustedWithOptions, kAXTrustedCheckOptionPrompt, kAXButtonRole #type: ignore
from ApplicationServices import AXUIElementCreateApplication, AXUIElementCopyAttributeValue#type: ignore
from ApplicationServices import kAXWindowsAttribute, kAXChildrenAttribute, kAXRoleAttribute, kAXTitleAttribute#type: ignore

#seeing if script has access to system through accessibility APIs
ok = AXIsProcessTrustedWithOptions({kAXTrustedCheckOptionPrompt: True})
print(bool(ok))  # True if you already granted, False otherwise

#pid change everytime the zoom app launches
pid=0
#looping through running applications for zoom's pid
for app in NSWorkspace.sharedWorkspace().runningApplications():
    if app.bundleIdentifier()=="us.zoom.xos":
        pid=app.processIdentifier()
        break

#finding the zoom AZ root and python list of all meeting windows
if pid:
    zoom_ax = AXUIElementCreateApplication(pid)
    error, windows = AXUIElementCopyAttributeValue(zoom_ax, kAXWindowsAttribute, None)
    print(error)#if value is 0 windows were successfully found
    print(windows)

'''
desc: given a window, find if it has a mute/unmute button button using depth first search (after popping an element, we push their children to top of stack)
arg:S
root: window to search through
wanted_titles: button titles to find
'''
def find_mute_button(root, wanted_titles={"Mute", "Unmute"}):
    stack=[root]#initialize the stack with one element, the window's root
    while stack:
        element = stack.pop()
        role = AXUIElementCopyAttributeValue(element, kAXRoleAttribute)
        #if the current element in the window being iterated through is a button, check for button text
        if role == kAXButtonRole:
            title = AXUIElementCopyAttributeValue(element, kAXTitleAttribute)
            if isinstance(title, str) and title in wanted_titles:
                return (element, title)

        #if the element's role is not a button, push it's children elements to the top of the stack
        children = AXUIElementCopyAttributeValue(element, kAXChildrenAttribute) or []
        stack.extend(children)

    #return nothing if no mute button is found
    return (None, None)


#recursively iterating through the windows to find the window with the mute button
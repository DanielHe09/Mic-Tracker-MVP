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
        break;

print(pid)
import sys
import site
import os
try:
    import flask_login
    print("--- Flask-Login Found ---")
    print(f"Location: {flask_login.__file__}")
except ImportError:
    print("--- Flask-Login NOT Found by this interpreter ---")

print("\n--- sys.path ---")
# Print the paths Python searches for modules
for p in sys.path:
    print(p)

# Print standard site-packages locations known to this interpreter
print("\n--- site packages ---")
try:
    print(site.getsitepackages())
except AttributeError:
    print("site.getsitepackages() not available")


print("\n--- user site packages ---")
try:
    print(site.getusersitepackages())
except AttributeError:
     print("site.getusersitepackages() not available")

print(f"\n--- Current Interpreter ---")
print(sys.executable) # Shows the exact python executable being run
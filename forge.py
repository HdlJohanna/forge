import requests
import json
import time
import shutil
import sys
import os

if len(sys.argv) < 2:
    print("Error: Invalid Arguments supplied")
    print("Check Help by running `forge help`")
    exit(1)

if __name__ != "__main__":
    exit(1)

sys.argv.pop(0)

packages = []
url = "http://archive.forge.repl.co" 

cmd = sys.argv.pop(0)

forgedir = os.path.dirname(os.path.expanduser("~"))+"/forge"

def addpath(path):
    if sys.platform == "win32":
        os.system(f"setx PATH=%PATH%;{path}")
    else:
        with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
            # 'a' stands for "append"  
            outfile.write(f"export PATH=$PATH:{path}")
        os.system(f". {os.path.expanduser('~/.bashrc')}")

if cmd == "pwd":
    print(f"Forge is located at {forgedir}")
    exit()

elif cmd == "help":
    print("-------- Forge 1.2.1 --------")
    print("The package Manager that was missing on Windows and MacOS (and Linux)")
    print("COMMANDS")
    print("install [packages]: Install Packages") 

elif cmd == "install":
    for arg in sys.argv:
        if arg.startswith("-"):
            continue

        packages.append(arg)

    for pkg in packages:
        tstart = time.time()
        r = requests.get(url+"/package?n="+pkg)
        meta = r.json()
        if "resp" in meta.keys():
            print(f"E: Package \"{pkg}\" doesn't exist")
        else:
            print(f"Get:{meta['url']}")
            r = requests.get(meta["url"])
            with open(forgedir+f"/{pkg}.tmp", "wb") as f:
                f.write(r.content)
            print(f"Downloaded Package in {time.time()-tstart} Milliseconds")
            shutil.unpack_archive(forgedir+f"/{pkg}.tmp", os.path.join(forgedir, pkg), "gztar")
            addpath(forgedir+f"/{pkg}")
            os.chdir(forgedir+f"/{pkg}")
            for r in meta["install"]:
                if "sys" in r:
                    syst, cmd = r.split("::")
                    os.system(cmd)
            print(f"Successfully installed {pkg}!")
    print(f"Successfully installed {len(packages)} Programs")

elif cmd == "tap":
    path = (sys.argv[-1])
    print(f"Tapping {path} to {forgedir}/{sys.argv[-1]}...")
    shutil.copytree(path, os.path.join(forgedir,sys.argv[-1]))
    addpath(os.path.join(forgedir,sys.argv[-1]))
    print(f"Successfully tapped {sys.argv[-1]}!")

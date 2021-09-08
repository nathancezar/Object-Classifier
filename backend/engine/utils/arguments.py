import sys
import argparse
import json

def getJson():
    try:
        arguments = json.loads(sys.argv[1])
        items = arguments['args'].split()

        arguments["objects"] = False
        arguments["clearing"] = False
        arguments["lane"] = False
        arguments["crack"] = False
        arguments["zebra"] = False
        arguments["third_lane"] = False
        arguments["roadside"] = False
        arguments["crosswalk"] = False

        for item in items:
            arguments[item] = True

        arguments["verbose"] = False
        arguments["save"] = True
        arguments["frame"] = 0
    except json.decoder.JSONDecodeError:
        return None
    else:
        return arguments

def getArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="path to input video")
    ap.add_argument("-o", "--objects", action="store_true", default=False, help="executes faster r-cnn")
    ap.add_argument("-c", "--clearing", action="store_true", default=False, help="executes clearing detector")
    ap.add_argument("-l", "--lane", action="store_true", default=False, help="executes lane detector")
    ap.add_argument("-k", "--crack", action="store_true", default=False, help="executes crack detector")
    ap.add_argument("-z", "--zebra", action="store_true", default=False, help="executes zebra lines detector")
    ap.add_argument("-t", "--third-lane", action="store_true", default=False, help="executes third lane detector")
    ap.add_argument("-r", "--roadside", action="store_true", default=False, help="executes roadside detector")
    ap.add_argument("-cw", "--crosswalk", action="store_true",default=False, help="executes crosswalk detector")
    ap.add_argument("--save", action="store_true", default=False, help="save the results")
    ap.add_argument("-f", "--frame", type=int, default=0, help="frame number from where to begin")
    ap.add_argument('--verbose', dest='verbose', action='store_true')
    ap.add_argument('--no-verbose', dest='verbose', action='store_false')
    ap.set_defaults(verbose=True)
    return vars(ap.parse_args())

def parseArguments():
    arguments = getJson()
    if not arguments:
        arguments = getArguments()
    try:
        arguments["frame"] = int(arguments["frame"])
        assert(arguments["frame"] >= 0)
    except:
        arguments["frame"] = 0

    return arguments

def getDefaultArguments():
    arguments = {}
    arguments["objects"] = True
    arguments["clearing"] = True
    arguments["lane"] = True
    arguments["crack"] = True
    arguments["zebra"] = True
    arguments["third_lane"] = True
    arguments["roadside"] = True
    arguments["crosswalk"] = True
    arguments["verbose"] = False
    arguments["save"] = True
    arguments["frame"] = 0
    return arguments
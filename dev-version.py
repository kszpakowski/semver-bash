import subprocess


def writeVersionToFile(tag):
    with open("version.env", "w") as file:
        file.write("VERSION="+tag)


def extractVersionElements(tag):
    return list(map(int, tag.replace("-dev", "").split(".")))


allTags = subprocess.run(["git", "tag", "--list", "--merged",
                          "HEAD"], capture_output=True).stdout.decode('ascii').split("\n")

devTags = list(filter(lambda tag: "dev" in tag, allTags))
rcTags = list(filter(lambda tag: "RC" in tag, allTags))

devTags.sort(key=extractVersionElements)

try:
    lastDevTag = devTags[-1]
    major, minor, patch, suffix = extractVersionElements(lastDevTag)

    try:
        # if RC tag for last dev tag is present return next minor version
        matchingRcTag = list(
            filter(lambda tag: f'{major}.{minor}.{patch}-RC' in tag, rcTags))[0]
        newVersion = f'{major}.{minor+1}.0-dev.1'
        writeVersionToFile(newVersion)
        exit()
    except IndexError:
        # RC tag is not present return next dev version
        newVersion = f'{major}.{minor}.{patch}-dev.{suffix+1}'
        writeVersionToFile(newVersion)

except IndexError:
    # Dev tag not found - return default tag and exit.
    writeVersionToFile("0.1.0-dev.1")
    exit()

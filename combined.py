import subprocess


def writeVersionToFile(tag):
    with open("version.env", "w") as file:
        file.write("VERSION="+tag)


def extractVersionElements(tag):
    return list(map(int, tag.replace("-dev", "").replace("-RC", "").split(".")))


def getTags():
    allTags = subprocess.run(["git", "tag", "--list", "--merged",
                              "HEAD"], capture_output=True).stdout.decode('ascii').split("\n")

    devTags = list(filter(lambda tag: "dev" in tag, allTags))
    devTags.sort(key=extractVersionElements)

    rcTags = list(filter(lambda tag: "RC" in tag, allTags))
    rcTags.sort(key=extractVersionElements)
    return(devTags, rcTags)


def nextDevTag():
    devTags, rcTags = getTags()
    try:
        lastDevTag = devTags[-1]
        major, minor, patch, suffix = extractVersionElements(lastDevTag)

        try:
            # if RC tag for last dev tag is present return next minor version
            matchingRcTag = list(
                filter(lambda tag: f'{major}.{minor}.{patch}-RC' in tag, rcTags))[0]
            newVersion = f'{major}.{minor+1}.0-dev.1'
            writeVersionToFile(newVersion)
        except IndexError:
            # RC tag is not present return next dev version
            newVersion = f'{major}.{minor}.{patch}-dev.{suffix+1}'
            writeVersionToFile(newVersion)

    except IndexError:
        # Dev tag not found - return default tag and exit.
        writeVersionToFile("0.1.0-dev.1")


def nextRcTag():
    devTags, rcTags = getTags()
    lastDevTag = devTags[-1]
    devMajor, devMinor, _, _ = extractVersionElements(lastDevTag)

    try:
        lastRcTag = rcTags[-1]

        rcMajor, rcMinor, rcPatch, rcSuffix = extractVersionElements(lastRcTag)

        if devMajor > rcMajor or (devMajor == rcMajor and devMinor > rcMinor):
            # Dev is never than last rc - create rc from dev
            writeVersionToFile(f"{devMajor}.{devMinor}.0-RC.1")
        else:
            # There is no newver dev version, increase RC suffix
            writeVersionToFile(
                f"{rcMajor}.{rcMinor}.{rcPatch}-RC.{rcSuffix+1}")

    except IndexError:
        # RC tag does not exist, create RC from last dev tag
        writeVersionToFile(f"{devMajor}.{devMinor}.0-RC.1")


def nextProdTag():
    _, rcTags = getTags()
    lastRcTag = rcTags[-1]

    rcMajor, rcMinor, rcPatch, _ = extractVersionElements(lastRcTag)

    writeVersionToFile(f"{rcMajor}.{rcMinor}.{rcPatch}")

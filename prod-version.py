import subprocess


def writeVersionToFile(tag):
    with open("version.env", "w") as file:
        file.write("VERSION="+tag)


def extractVersionElements(tag):
    return list(map(int, tag.replace("-dev", "").replace("-RC", "").split(".")))


allTags = subprocess.run(["git", "tag", "--list", "--merged",
                          "HEAD"], capture_output=True).stdout.decode('ascii').split("\n")

rcTags = list(filter(lambda tag: "RC" in tag, allTags))
rcTags.sort(key=extractVersionElements)

lastRcTag = rcTags[-1]

rcMajor, rcMinor, rcPatch, _ = extractVersionElements(lastRcTag)

writeVersionToFile(f"{rcMajor}.{rcMinor}.{rcPatch}")

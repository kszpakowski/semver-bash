import subprocess

def writeVersionToFile(tag):
    with open("version.env", "w") as file:
      file.write("VERSION="+tag)

allTags = subprocess.run(["git", "tag", "--list", "--merged",
                          "HEAD"], capture_output=True).stdout.decode('ascii').split("\n")

devTags = list(filter(lambda tag: "dev" in tag , allTags))
rcTags = list(filter(lambda tag: "RC" in tag , allTags))

devTags.sort(key=lambda tag: tag.split("."))

try:
    lastDevTag = devTags[-1]
except IndexError:
    # Dev tag not found - return default tag and exit.
    writeVersionToFile("0.1.0-dev.1")
    exit()

baseAndSuffix = lastDevTag.split("-")
versionBase = baseAndSuffix[0]
versionSuffix = baseAndSuffix[-1]

majorMinorPatch = versionBase.split(".")
major = int(majorMinorPatch[0])
minor = int(majorMinorPatch[1])

try:
    patch = int(majorMinorPatch[2])
except IndexError:
    patch = 0

suffixVersion = int(versionSuffix.split(".")[-1])

# calculate next version
try:
  # if RC tag for last dev tag is present return next minor version 
  matchingRcTag = list(filter(lambda tag: f'{major}.{minor}.{patch}-RC' in tag , rcTags))[0]
  newVersion = f'{major}.{minor+1}.0-dev.1'
  writeVersionToFile(newVersion)
  exit()
except IndexError:
    # if RC tag is not present return next dev version
    newVersion = f'{major}.{minor}.{patch}-dev.{suffixVersion+1}'
    writeVersionToFile(newVersion)
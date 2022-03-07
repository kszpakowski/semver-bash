import subprocess


def cleanupTags():
    print("cleanup tags")
    subprocess.run(["sh", "-c", "git tag | xargs git tag -d"])


def listTags():
    tags = subprocess.run(["sh", "-c", "git tag --list"],
                          capture_output=True).stdout.decode('ascii')
    print("tags:" ,tags)
    return tags


def generateNextDevTag():
    print("generateDevTag")
    subprocess.run(["python", "dev-version.py"])
    with open("version.env", "r") as file:
        devTag = file.readline().split("=")[-1]
        print(f"tag with new tag {devTag}")
        subprocess.run(["sh", "-c", "git tag "+devTag])
        return devTag


def generateTag(tag):
    print(f"tag with new tag {tag}")
    subprocess.run(["sh", "-c", "git tag "+tag])
    return tag


cleanupTags()

print("generate first tag")
tag = generateNextDevTag()
listTags()
assert(tag == "0.1.0-dev.1")

print("generate next dev tag")
tag = generateNextDevTag()
listTags()
assert(tag == "0.1.0-dev.2")

print("generate next dev tag")
tag = generateNextDevTag()
listTags()
assert(tag == "0.1.0-dev.3")

print("generate RC tag")
tag = generateTag("0.1.0-RC.1")
listTags()
assert(tag == "0.1.0-RC.1")

print("generate first dev tag after RC")
tag = generateNextDevTag()
listTags()
assert(tag == "0.2.0-dev.1")

print("generate second dev tag after RC")
tag = generateNextDevTag()
listTags()
assert(tag == "0.2.0-dev.2")
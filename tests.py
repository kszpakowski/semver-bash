import subprocess


def cleanupTags():
    print("cleanup tags")
    subprocess.run(["sh", "-c", "git tag | xargs git tag -d"])


def listTags():
    tags = subprocess.run(["sh", "-c", "git tag --list"],
                          capture_output=True).stdout.decode('ascii')
    print("tags:", tags)
    return tags


def generateNextDevTag():
    subprocess.run(["python", "dev-version.py"])
    with open("version.env", "r") as file:
        devTag = file.readline().split("=")[-1]
        print(f"tag with new tag {devTag}")
        subprocess.run(["sh", "-c", "git tag "+devTag])
        return devTag


def generateNextRcTag():
    subprocess.run(["python", "rc-version.py"])
    with open("version.env", "r") as file:
        tag = file.readline().split("=")[-1]
        print(f"tag with new tag {tag}")
        subprocess.run(["sh", "-c", "git tag "+tag])
        return tag

def generateNextProdTag():
    subprocess.run(["python", "prod-version.py"])
    with open("version.env", "r") as file:
        tag = file.readline().split("=")[-1]
        print(f"tag with new tag {tag}")
        subprocess.run(["sh", "-c", "git tag "+tag])
        return tag


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
tag = generateNextRcTag()
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


print("generate second dev tag after RC")
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
generateNextDevTag()
tag = generateNextDevTag()
listTags()
assert(tag == "0.2.0-dev.12")

print("generate second RC tag")
tag = generateNextRcTag()
listTags()
assert(tag == "0.2.0-RC.1")

print("generate next RC tag")
tag = generateNextRcTag()
listTags()
assert(tag == "0.2.0-RC.2")

print("generate dev tag after second RC")
tag = generateNextDevTag()
listTags()
assert(tag == "0.3.0-dev.1")

print("generate 0.3.0 RC tag")
tag = generateNextRcTag()
listTags()
assert(tag == "0.3.0-RC.1")

print("generate 0.3.0 prod tag")
tag = generateNextProdTag()
listTags()
assert(tag == "0.3.0")

print("generate 0.4.0-dev.1 tag")
tag = generateNextDevTag()
listTags()
assert(tag == "0.4.0-dev.1")

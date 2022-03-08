import subprocess, re

tags = subprocess.run(["git", "tag"],
                      capture_output=True).stdout.decode('ascii').split("\n")

#Add missing patch version
for tag in tags: 
    if re.match("\d\.\d-", tag):
        rev = subprocess.run(["git", "rev-list", "-n", "1", f"tags/{tag}"],capture_output=True).stdout.decode("ascii")

        # Tag same revision with the same version but with default patch part included
        subprocess.run(["git","tag","-a",tag.replace("-",".0-"),rev[0:7],"-m",f"Replaced invalid semver tag: {tag}"])
        print(rev)
        # remove invlaid tag
        subprocess.run(["git","tag","-d",tag])
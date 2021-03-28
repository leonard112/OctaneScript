import sys
import subprocess
import hashlib


invalid_sha256sums_found = False

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def validate_checksums_for_release(github_release_tag, sourceforge_release_folder):
    subprocess.run(f"curl -L -O https://github.com/leonard112/OctaneScript/releases/download/{github_release_tag}/SHASUMS256.txt.asc", stdout=None, stderr=None, shell=True)
    sha256_checksums = open("SHASUMS256.txt.asc").readlines()

    print(f"\n{YELLOW}Validating sha256 checksums for OctaneScript release '{github_release_tag}'...")
    for line in sha256_checksums:
        file_tokens = line.strip().split()
        file_name = file_tokens[1]
        expected_sha256 = file_tokens[0]
        file_extension = file_name.split(".")[-1]

        if file_extension == "deb":
            package_type = "debian"
        elif file_extension == "tgz":
            package_type = "tar"
        elif file_extension == "exe":
            package_type = "installer"
        elif file_extension == "zip":
            package_type = "zip"
        
        if file_name.find("windows") != -1:
            os = "windows"
        else:
            os = "linux"

        subprocess.run(f"curl -L -O https://github.com/leonard112/OctaneScript/releases/download/{github_release_tag}/{file_name}", stdout=None, stderr=None, shell=True)
        actual_github_release_sha256 = hashlib.sha256(open(file_name, 'rb').read()).hexdigest()
        subprocess.run(f"rm {file_name}", stdout=None, stderr=None, shell=True)
        subprocess.run(f"curl -L -O https://downloads.sourceforge.net/project/octanescript/{sourceforge_release_folder}/{os}/amd64/stable/{package_type}/{file_name}", stdout=None, stderr=None, shell=True)
        actual_sourceforge_release_sha256 = hashlib.sha256(open(file_name, 'rb').read()).hexdigest()
        
        if expected_sha256 != actual_github_release_sha256 or expected_sha256 != actual_sourceforge_release_sha256:
            global invalid_sha256sums_found
            invalid_sha256sums_found = True
            message = "Checksums do not match"
            color = RED
        else:
            message = "Ok"
            color = GREEN

        print(f"""{color}{file_name}:
    Expected Sha256: {expected_sha256}
    Actual GitHub Sha256: {actual_github_release_sha256}
    Actual SourceForge Sha256: {actual_sourceforge_release_sha256}
    {message}""")
        subprocess.run(f"rm {file_name}", stdout=None, stderr=None, shell=True)
    subprocess.run("rm SHASUMS256.txt.asc", stdout=None, stderr=None, shell=True)


validate_checksums_for_release("0.0.4-alpha", "alpha")
validate_checksums_for_release("0.0.5-alpha", "alpha")
    
if invalid_sha256sums_found == True:
    exit(1)

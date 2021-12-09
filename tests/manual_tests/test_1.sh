set -x
rm -rf test_repo
mkdir test_repo
cd test_repo
hit init
touch file1 ; touch file2 ; touch file3
hit add file1
hit status
hit add *
hit status

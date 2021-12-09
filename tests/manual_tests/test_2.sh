set -x
dir_name=test_repo_456
rm -rf $dir_name
mkdir $dir_name
cd $dir_name
hit init
touch file1 && touch file2
hit status
hit add file1 && hit status
hit commit && hit status
echo 'test' >> file1 && hit status
hit add file1 && hit commit && hit status
hit add * && hit commit && hit status

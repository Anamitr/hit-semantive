sh uninstall.sh
mkdir ~/.hit_install
cp -r * ~/.hit_install
chmod u+x ~/.hit_install hit
# Make globally available
PATH=$PATH:~/.hit_install
echo '# Hit Semantive' >> ~/.bashrc
echo 'export PATH="${PATH}:$HOME/.hit_install"' >> ~/.bashrc

echo Hit has been installed to you HOME dir and added to path
echo You can try it by typing 'hit' in console


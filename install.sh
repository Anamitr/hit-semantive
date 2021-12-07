sh uninstall.sh
mkdir ~/.hit_install
cp -r * ~/.hit_install
chmod u+x ~/.hit_install hit
# Make globally available
echo '# Hit Semantive' >> ~/.bashrc
echo 'export PATH="${PATH}:$HOME/.hit_install"' >> ~/.bashrc

echo Hit has been installed to you HOME dir and added to path
echo Create new console or source ~/.bashrc to use it
echo You can try it by typing 'hit'


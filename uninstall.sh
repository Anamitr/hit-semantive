rm -rf ~/.hit_install
sed -ni '/# Hit Semantive/!p' ~/.bashrc
sed -ni '/export PATH="\${PATH}:\$HOME\/\.hit_install"/!p' ~/.bashrc


```
objective: 

in ubuntu, setup custom urls so chrome will open itksnap

ref

https://unix.stackexchange.com/questions/497146/create-a-custom-url-protocol-handler
https://deluge.readthedocs.io/en/latest/how-to/set-mime-type.html
https://help.gnome.org/admin/system-admin-guide/stable/mime-types-custom-user.html.en
https://askubuntu.com/questions/62585/how-do-i-set-a-new-xdg-open-setting

https://superuser.com/questions/162092/how-can-i-register-a-custom-protocol-with-xdg
```


```

# make executable and application files

sudo cp citksnap.sh /usr/bin
sudo chmod +x /usr/bin/citksnap.sh

sudo cp citksnap.desktop /usr/share/applications
sudo chmod 664 /usr/share/applications/citksnap.desktop

#setup custom mime type

xdg-mime default citksnap.desktop x-scheme-handler/citksnap
gio mime x-scheme-handler/citksnap citksnap.desktop

update-mime-database ~/.local/share/mime
update-desktop-database ~/.local/share/applications

#confirm

xdg-mime query default x-scheme-handler/citksnap

#(option) confirm
gio mime x-scheme-handler/citksnap 

# test open

xdg-open itksnap://123123


```

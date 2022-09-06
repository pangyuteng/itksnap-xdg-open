
```
objective: 

in ubuntu, setup custom urls so chrome will open itksnap

ref

https://unix.stackexchange.com/questions/497146/create-a-custom-url-protocol-handler

https://askubuntu.com/questions/62585/how-do-i-set-a-new-xdg-open-setting

https://superuser.com/questions/162092/how-can-i-register-a-custom-protocol-with-xdg
```


```

# make executable and application files

sudo chmod +x citksnap.sh
sudo cp citksnap.sh /usr/bin
sudo cp citksnap.desktop /usr/share/applications

#setup custom mime type

xdg-mime default citksnap.desktop x-scheme-handler/citksnap

#confirm

xdg-mime query default x-scheme-handler/citksnap

# test open

xdg-open itksnap://123123


```

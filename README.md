
#### project summary:

In ubuntu-desktop, setup custom uri so chrome will load images and contours to a PyQt window and ITKSNAP within a docker container.

Checkout the corresponding youtube clip for a step by step tutorial.
https://www.youtube.com/watch?v=l3LyFTeypb0


for example in chrome:

```
citksnap://image_file=/demo-image/dcm&segmentation_file=/demo-image/contours.nii.gz&workdir=/demo-image
```

or run below in terminal:

```
xdg-open citksnap://image_file=/demo-image/dcm&segmentation_file=/demo-image/contours.nii.gz&workdir=/demo-image
```

or for devs, run .sh in terminal:

```
cd gnome
bash citksnap.sh citksnap://image_file=/demo-image/dcm&segmentation_file=/demo-image/contours.nii.gz&workdir=/demo-image
```

#### setup


+ build container

```
cd docker
bash build.sh
```

+ make executable and application files

```
sudo cp gnome/citksnap.sh /usr/bin
sudo chmod +x /usr/bin/citksnap.sh

sudo cp gnome/citksnap.desktop /usr/share/applications
sudo chmod 664 /usr/share/applications/citksnap.desktop

```

+ setup custom mime type

```
xdg-mime default citksnap.desktop x-scheme-handler/citksnap
update-desktop-database ~/.local/share/applications
```

+ confirm app linking is setup

```
xdg-mime query default x-scheme-handler/citksnap
```

+ ?? likely unecessary
```
gio mime x-scheme-handler/citksnap citksnap.desktop
update-mime-database ~/.local/share/mime
gio mime x-scheme-handler/citksnap 
```

+ click demo url in chrome:

```
chromium index.html
```

+ for actual deployment, update docker volume path in below file and correspondingly, paths in uri `citksnap://` for all production sites.

```
gnome/citksnap.sh
```




### references

```
https://unix.stackexchange.com/questions/497146/create-a-custom-url-protocol-handler
https://deluge.readthedocs.io/en/latest/how-to/set-mime-type.html
https://help.gnome.org/admin/system-admin-guide/stable/mime-types-custom-user.html.en
https://askubuntu.com/questions/62585/how-do-i-set-a-new-xdg-open-setting
https://superuser.com/questions/162092/how-can-i-register-a-custom-protocol-with-xdg
```



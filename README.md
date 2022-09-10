
project goal:

in ubuntu gnome, setup custom urls so chrome will open itksnap within docker.

for example in chrome:

```
citksnap://dicom_folder=/mydownloads/2020-fibrosis/dcm,segmentation_file=/mydownloads/2020-fibrosis/nice.nii.gz
```


or run below in terminal:

```
xdg-open citksnap://dicom_folder=/mydownloads/2020-fibrosis/dcm,segmentation_file=/mydownloads/2020-fibrosis/nice.nii.gz
```

or for devs, run .sh in terminal:

```
cd gnome
bash citksnap.sh citksnap://dicom_folder=/mydownloads/2020-fibrosis/dcm,segmentation_file=/mydownloads/2020-fibrosis/nice.nii.gz
```

ref
```
https://unix.stackexchange.com/questions/497146/create-a-custom-url-protocol-handler
https://deluge.readthedocs.io/en/latest/how-to/set-mime-type.html
https://help.gnome.org/admin/system-admin-guide/stable/mime-types-custom-user.html.en
https://askubuntu.com/questions/62585/how-do-i-set-a-new-xdg-open-setting

https://superuser.com/questions/162092/how-can-i-register-a-custom-protocol-with-xdg
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
gio mime x-scheme-handler/citksnap citksnap.desktop

update-desktop-database ~/.local/share/applications
```

+ confirm app linking is setup

```
xdg-mime query default x-scheme-handler/citksnap
```

+ ?? likely unecessary
```
update-mime-database ~/.local/share/mime
gio mime x-scheme-handler/citksnap 
```

+ click demo url in chrome:

```
chromium index.html
```


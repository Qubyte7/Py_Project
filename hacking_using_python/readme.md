# REVERSE SHELL CONNECTION USING Python
## this project encompesse with establishing reverse shell using python
### step involved
1. Know the Ip address of the client 
2. specify the port number for establishing connections
3. compile the reverse shell codes
4. cover the *executable file* with an Ico Image or PDF
5. you can also further upgrade your attack to by pass firewall


## some commands involved 
### <ins>description</ins>
For a better reverse shell persistence you must detach it from the command line 
bellow are the commands you can use to check and terminate the ncat connection it you want

***check ncat connection*** :   <sup>tasklist | findstr "ncat" </sup> *(windows)*
                                <sup>tasklist | grep "ncat" </sup> *(linux)*

***terminate ncat connection*** :   <sup>taskkill /IM ncat.exe /F </sup> *(windows)*
                                    <sup>pkill firefox </sup> *(linux)* 


## For disguissing our *executable_file* we use **pyinstaller** 
### covering our *executable_file* icon image
***command*** : **<sub>pyinstaller --onefile --noconsole --icon= < Your_Image_icon.ico >  --distpath < path to the storage > < your_script.py > </sub>**

**flag explanation** : 
🔹 --distpath → Final .exe location.
🔹 --workpath → Temporary PyInstaller files.

<ins> example of command </ins>

pyinstaller --onefile --noconsole --icon=./images/cover.ico --distpath "C:\Users\user\Downloads\cybersec\Py_Project\hacking_using_python\final_output" --workpath "C:\Users\user\Downloads\cybersec\Py_Project\hacking_using_python\final_output" reverse_shell.py


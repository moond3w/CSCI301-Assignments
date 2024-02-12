<h3>Program Information</h3><br>
<b>Python Version:</b> 3.10.12<br>
<b>Packages Needed:</b> PyCryptodome (https://www.pycryptodome.org/)<br>
<br>
<b>Program Description:</b><br>
<p>
Two programs can be found in the folder: “a1_encryption.py” and “a2_decryption.py”. 
The first program encrypts all files with the extension “.txt” in the current directory to “&lt;filename.txt&gt;.encrypted”. A session key is generated for each file and encrypted via RSA encryption to “&lt;filename.txt&gt;.session_key.bin”.
</p>
<p>The command to execute the script is as follows: </p>
<code>python3 a1_encryption.py</code><br>

<p>
The second program decrypts the session keys with the corresponding RSA private key and then proceeds to use the session key to decrypt the corresponding “.encrypted” files back to text files with the following extension “&lt;filename.txt&gt;.decrypted”.
</p>
<p>The command to execute the script is as follows: </p>

<code>python3 a1_decryption.py</code>


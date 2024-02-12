<h3>Program Information</h3><br>
<b>Python Version:</b> 3.10.12<br>
<b>Packages Needed:</b> PyCryptodome (https://www.pycryptodome.org/)<br>
<br>
<b>Program Description:</b><br>
<p>
There are two programs in the folder, csci301_a2.py and csci301_a2_execute.py. There is also a public_key.pem which contains the domain parameters p, q, g 
  that is required to be used in both programs.
</p>
<p>
csci301_a2.py simulates the P2MS script by taking 2 parameters: the number of signatures <b>M</b>, and the number of public keys <b>N</b>. 
  <b>N</b> sets the number of DSA 1024 bits public/private keys to be randomly generated in scriptPubKey.txt, while <b>M</b> sets the number of 
  signatures to be signed by the DSA keys generated earlier and written to scriptSig.txt. The text “CSCI301 Contemporary topic in security 2024” 
  is used as the text signed by all the signatures. It is required for <b>N</b> is greater than or equal to <b>M</b>. The command to execute the script is as follows: 
</p>
	
<code>python3 csci301_a2.py #M #N</code>
	
<p>
csci301_a2_execute.py executes the P2MS script by taking the two files scriptSig.txt and scriptPubKey.txt and combining the files into a stack. 
The program then executes a sanity check on the stack to ensure that there are <b>M</b> signatures and <b>N</b> public keys in the stack. 
Finally, the program executes OP_CHECKMULTISIG, which pops out the elements and checks whether the signatures are valid. The script then pushes either 
  “1” or “0” to signify whether the signatures were verified successfully, as well as displaying a message to notify the user. The command to execute the script is as follows:
</p>

<code>python3 csci301_a2_execute.py</code>
	
<p>The files scriptSig.txt and scriptPubKey.txt must exist for the program to run successfully (from executing csci301_a2.py).</p>
 

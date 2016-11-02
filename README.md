# LHE-Codec-Audio



This is a python audio coder-decoder using the LHE algorithm. It will codify amplitude hops, and will use Huffman coding to represent them as symbols. This is a version of the image codec using the same algorithm.



## Image codec project



You can check the image codec project in Python here: *https://github.com/Lykaos/LHE-Codec*

Also, you can check a more optimized C version of it here: *https://github.com/magonzalezc/LHE*



## More info



You can learn more about LHE in this article: *http://oa.upm.es/37459/1/INVE_MEM_2014_200038.pdf*



## How to install (Windows)



1. Install Python 2.7 and the IDLE Editor if you dont have them in your computer.

2. Now we need to install the wave module. Wave is a Python module which works with audio (opening, loading, getting sample values, etc). Open a command prompt (cmd) in administrator mode, go to the path you installed Python (if you dont have it in environment variables) and type:

  ```
  pip install wave
  ```

3. Open the IDLE editor with example.py and execute it with the F5 key or the Run menu.



## How to install (Linux)



1. Install Python 2.7 if you dont have it in your computer.

2. Open a new terminal and type:

  ```
  sudo apt-get install python-pip
  sudo pip install wave
  ```

3. Go to the path where example.py is and execute it with the command:

  ```
  python example.py
  ```


## How to use

The example program ("example.py") will ask you what do you want to do. Type *enc* for encoding or *dec* for decoding. You can also type *exit* to close the program.



### Encoding

Once you selected encoding, the program will ask you the audio you want to work with. This codec only works with audios which are saved in the input_audio folder, be sure to save and select one from there. You will know when the program succesfully finishes the encoding.

### Decoding

The program won't ask you anything if you select decoding. You must have a .lhe file in the output_lhe folder (generated by the encoder) and it will create the audio file in the output_audio folder. If you want to decode an external .lhe file, be sure to rename it to lhe_file.lhe and save it in the output_lhe folder. You will know when the program succesfully finishes the decoding.
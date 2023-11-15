# Fingerprint_Authentication
The proposed  fingerprint identification system consists of different phases, namely:-1. Fingerprint Liveliness 2. Fingerprint acquisition, 2. Finger markup & matching.
Images can be acquired through a control capture device such as a scanner or a fixed focus camera. The image acquisition provides a perceived dpi (dots per inch) measurement to adjust the image resolution. 
The image dpi captured using a live-scanner is different from the image which is collected.
 Pre-processing of the fingerprints including reconstruction (Direct denoise the fingerprints and reconstruct the missing ridge structure without explicitly estimating the orientation field using GAN’s and CNN-based fingerprint reconstruction from the corrupted image)
 Fingerprint feature extraction, is the further step.
The last step is fingerprint matching from the database.


The main objective was using ML algorithm to find out whether the input fingerprint is real or fake 


Fake fingerprint can be created using various techniques
namely
**Gelatin or Silicone Mold:** Creating a mold of a fingerprint using gelatin, silicone, or other moldable materials. This can be used to imprint the fingerprint onto other surfaces.

**Latex or Glue Mold:** Similar to the gelatin method, using liquid latex or glue to capture the fingerprint and create a mold for replication.

**3D Printing:** Advanced technology allows for the creation of detailed fingerprint replicas using 3D printing techniques. A real fingerprint can be scanned and replicated onto a surface.

**Biometric Spoofing:** This involves using advanced materials such as conductive ink, gels, or other substances to replicate a real fingerprint's electrical properties. These materials can deceive some biometric scanners that detect the electrical conductivity of the skin.

**Adhesive Lifts:** Lifting latent fingerprints from surfaces using adhesive materials such as fingerprint tape or gel lifters, and then transferring these lifted prints onto another surface.

**Computer-Generated:** Utilizing computer software to digitally generate fake fingerprints based on statistical models or collected data.

**Master Fingerprints:** Creating a master print that might mimic multiple fingerprints, exploiting weaknesses in some fingerprint recognition systems.

**Synthetic Skin:** Developing synthetic materials that mimic the texture, flexibility, and conductivity of human skin to deceive biometric systems.

We had to make a ML algo which can expose the fake the fingerprint 


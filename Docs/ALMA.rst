=========================
ALMA RASCIL vs. ALMA CASA
=========================

This documentation offers CASA vs. RASCIL scripts on ALMA datasets, for results comparison:

-   [1]_ ALMA RASCIL

-   [2]_ ALMA CASA

Three ALMA datasets are already uploaded under LFN, these are: HLTau_Band6, HLTau_Band7 and Mira_Band6.


ALMA RASCIL
===========

-  Scripts:

   Folder alma_rascil with all scripts [3]_ Download files and submit to IRIS three jobs, by using the below command:
 
.. code:: python


   $ dirac-wms-job-submit alma_rascil.jdl

   
   
ALMA CASA
===========

-  Scripts:

   Folder alma_casa with all scripts [4]_ Download files and submit to IRIS three jobs, by using the below command:
   
.. code:: python


   $ dirac-wms-job-submit alma_casa.jdl 

   
.. [1]
   https://ska-telescope.gitlab.io/external/rascil/installation/RASCIL_docker.html#singularity

.. [2]
   https://casaguides.nrao.edu/index.php/ALMA2014_LBC_SVDATA
   
.. [3]
   https://github.com/cimpan91/Docs/tree/main/Docs/alma_rascil
   
.. [4]
   https://github.com/cimpan91/Docs/tree/main/Docs/alma_casa

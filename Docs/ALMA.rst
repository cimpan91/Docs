=====================================================
Parameterized jobs - ALMA RASCIL vs. ALMA CASA tests
=====================================================

This documentation offers CASA vs. RASCIL scripts on ALMA datasets, for results comparison:

-   `ALMA_RASCIL <https://ska-telescope.gitlab.io/external/rascil/installation/RASCIL_docker.html#singularity>`__

-   `ALMA_CASA <https://casaguides.nrao.edu/index.php/ALMA2014_LBC_SVDATA>`__

Three ALMA datasets are already uploaded under LFN, these are: HLTau_Band6, HLTau_Band7 and Mira_Band6. ALMA datasets are stored under LFN as: %s_CalibratedData.tgz, where %s is the name of the parameter: 

.. code:: python


   Parameters = {"HLTau_Band6","HLTau_Band7","Mira_Band6"};

   see the parameters in the .jdl 


ALMA RASCIL
===========

-  Scripts:

   Folder `alma_rascil <https://github.com/cimpan91/AlmaTests/tree/main/alma_rascil>`__ contains all scripts. Download files and submit to IRIS three jobs, by using the below command:
 
.. code:: python


   $ dirac-wms-job-submit alma_rascil.jdl

   
   
More parameters can be added to the Parameters={"HLTau_Band6",,,,} list above, along with the ALMA datasets and their own configuration files. See example config files in configfiles.tar.gz. The steps, to add another dataset to be processed, are:
	- download ALMA dataset and store it under LFN with the name %s_CalibratedData.tgz (%s being one of the parameters, eg. HLTau_Band6)
	- create a configuration file for this dataset and add it to the configfiles.tar.gz
	- add the new parameter to the list of parameters in the .jdl file, Parameters = {"HLTau_Band6","HLTau_Band7","Mira_Band6"};
 
 
ALMA RASCIL tests are using a RASCIL container build from a recipe to enable the usage of config files. An example of recipe file that can be used is: 
 
 
 .. code:: python
 
    recipe file that uses an already pulled local RASCIL container: RASCIL-fullN.img
    
    $ cat SingRascilCasa.recipe 
    bootstrap: localimage 
    from: /home/<user>/RASCIL-fullN.img 
    %post
	cd /var/lib
	git clone https://github.com/casacore/casacore
	apt-get update && \
           apt-get -y install sudo	
	sudo apt-get -y install build-essential cmake gfortran g++ libncurses5-dev \
   		libreadline-dev flex bison libblas-dev liblapacke-dev libcfitsio-dev \
   		wcslib-dev libfftw3-dev
	sudo apt-get -y install libhdf5-serial-dev python-numpy \
   		 libboost-python-dev libpython3.7-dev  libpython2.7-dev
	cd casacore
	mkdir build
	cd build
	cmake ..
	make
	make install
 
 
     building the new container from recipe uses the command:
     
     $ sudo singularity build  RASCIL-full.img SingRascilCasa.recipe
   
   
ALMA CASA
===========

-  Scripts:

   Folder `alma_casa <https://github.com/cimpan91/AlmaTests/tree/main/alma_casa>`__ contains all scripts. Download files and submit to IRIS three jobs, by using the below command:
   
.. code:: python


   $ dirac-wms-job-submit alma_casa.jdl 

   
ALMA CASA scripts have been downloaded and their name has been changed to %s_Imaging.py, where %s is the name of the parameter (because of use of parametrized jobs). The files will be then archived into imgfiles.tar. These scripts are using the ALMA datasets %s_CalibratedData.tgz mentioned above.



RESULTS HLTau_Band6 DATASET
============================

These are the results for HLTau_Band6 DATASET `ALMA_RASCIL <https://github.com/cimpan91/AlmaTests/tree/main/results%20HLTAU6%20rascil>`__  and `ALMA_CASA <https://github.com/cimpan91/AlmaTests/tree/main/results%20HLTAU6%20casa>`__ 
Two fits images (RASCIL vs CASA outputs) converted to png are being shown below:

- RASCIL output `png <https://github.com/cimpan91/AlmaTests/blob/main/ical_restored_image_for_HL_Tau.png>`__  (conversion of output image ical_restored_image_for_HL_Tau.fits)

- CASA output `png <https://github.com/cimpan91/AlmaTests/blob/main/HLTau_B6cont_mscale_ap.image.png>`__  (conversion of output image HLTau_B6cont_mscale_ap.image.fits)


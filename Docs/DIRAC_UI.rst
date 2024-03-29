=============================
DIRAC install and basic usage
=============================

Introduction

-  IRIS resources

-  get a grid certificate

-  join VO (Virtual Organisation)

-  access DIRAC in browser

-  install DIRAC UI

-  submit a job (python –version)

-  monitor a job

-  put data on the file catalog

-  submitting RASCIL job

-  get output data RASCIL job

-  useful links  




IRIS resources `What_is_IRIS <https://www.iris.ac.uk/>`__

Get A Grid Certificate

-  a grid certificate is a .p12 file

-  Using your browser of choice visit `this page <https://portal.ca.grid-support.ac.uk>`_ and select the Request
   New User Certificate option. This almost goes without saying, but
   make sure you supply a valid email address which you can access. You
   will also be asked to do things like supply a PIN and passwords that
   you will need later on, so make sure you write everything down!

-  You will need to select a Registration Authority (RA) as part of this
   process.You may also be asked to supply a letter of recommendation
   explaining why you need to use the grid and with whom you will be
   working.

-  Details at    `grid_certificate <http://hep.ph.liv.ac.uk/~sjones/user-guides/getting-on-the-grid/grid-certificate.html>`__

Join a VO

-  Your grid certificate identifies you to the grid as an individual
   user, but it’s not enough on its own to allow you to use grid
   resources; you also need to join a Virtual Organisation (VO).

-  Note: I have made my request to skatelescope.eu - see   `Approved_Global_VOs <https://www.gridpp.ac.uk/wiki/GridPP_approved_VOs>`__

-  add the certificate to your browser and use the below link to register  `register_for_a_VO <https://voms.gridpp.ac.uk:8443/voms/skatelescope.eu/user/home.action>`__

Access DIRAC in browser

-  Now that you have the certificate and have joined to VO, you can add certificate to your browser and access DIRAC in browser   `DIRAC_in_browser <https://dirac.gridpp.ac.uk:8443/DIRAC/>`__

-  More details about DIRAC at Guide to DIRAC  `Guide_to_DIRAC <https://www.gridpp.ac.uk/wiki/Quick_Guide_to_Dirac#Server_URL>`__

DIRAC in Browser

.. figure:: DIRAC.png
   :alt: DIRAC

   

Before DIRAC install
====================

Overview of directories on your server

.. code:: python

   /home/<your-user> - home directory

   /raid/scratch/<your-user> - a working directory, here DIRAC will be installed

   FC:/............................ - belongs to IRIS, can store large data. You need DIRAC installation to
   be able to copy files to FC:/ (IRIS)

DIRAC install
==============

**Step 1:**  

.. code:: python
    
   - Switch to bash eg
   bash-4.2$ cat .bash_profile 
     #switch to bash
   setenv SHELL /usr/bin/bash
   exec /usr/bin/bash --login 
   
   bash-4.2$ /raid/scratch/<your-user> > mkdir dirac_ui
   bash-4.2$ /raid/scratch/<your-user> > cd dirac_ui/
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > mkdir $HOME/.globus
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui >ls
   certBundle.p12
   #make sure you have the cert in this folder dirac_ui, eg certBundle.p12



**Step 2:**  

.. code:: python

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > openssl pkcs12 -in certBundle.p12 -clcerts -nokeys -out $HOME/.globus/usercert.pem
   Enter Import Password:
   MAC verified OK
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > openssl pkcs12 -in certBundle.p12 -nocerts -out $HOME/.globus/userkey.pem
   Enter Import Password:
   MAC verified OK
   Enter PEM pass phrase:
   Verifying - Enter PEM pass phrase:
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > chmod 0400 $HOME/.globus/userkey.pem



**Step 3:**  

.. code:: python

  bash-4.2$ /raid/scratch/<your-user>/dirac_ui > wget -np -O dirac-install https://raw.githubusercontent.com/DIRACGrid/management/master/dirac-install.py --no-check-certificate
  bash-4.2$ /raid/scratch/<your-user>/dirac_ui > chmod u+x dirac-install
  bash-4.2$ /raid/scratch/<your-user>/dirac_ui > ./dirac-install -r v7r1p45



**Step 4:**  

.. code:: python

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > source bashrc
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-proxy-init -x -N
   Generating proxy...
   Enter Certificate password:
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > export X509_VOMS_DIR="$DIRAC/etc/grid-security/vomsdir"
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > export X509_VOMSES="$DIRAC/etc/grid-security/vomses"
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-configure -F -S GridPP -C dips://dirac01.grid.hep.ph.ic.ac.uk:9135/Configuration/Server -I
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-proxy-init -g skatelescope.eu_user -M -U 
   #skatelescope.eu it is the VO I am assigned to
   Generating proxy...
   Enter Certificate password:



Submit a simple job
====================

**Details at:**  `Simple_Job <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/CommandLine/index.html>`__

.. code:: python

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > cat simple.jdl
   JobName = "InputAndOuputSandbox";
   Executable = "pythonV.sh";
   StdOutput = "StdOut";
   StdError = "StdErr";
   InputSandbox = {"pythonV.sh"};
   OutputSandbox = {"StdOut","StdErr"};

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > cat pythonV.sh
   #!/bin/bash
   /usr/bin/python --version;


Monitor a simple job
=====================

**Details at:**  `Simple_Job <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/CommandLine/index.html>`__

.. code:: python

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-wms-job-submit simple.jdl
   JobID = 25104301

   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-wms-job-status 25104301
   JobID=25104301 Status=Done; MinorStatus=Execution Complete;
   Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

- The job execution can be seen also on DIRAC `Web-link <https://dirac.gridpp.ac.uk:8443/DIRAC/>`__
(see Applications/Job Monitor -> Owner (your name) -> submit)

Put RASCIL.img in a file catalog
================================

**Details at:**  `File_Catalog <https://dirac.readthedocs.io/en/latest/UserGuide/CommandReference/DataManagement/index.html>`__

.. code:: python
   
   - Accessing File Catalog to add a testFile or a singularity container
   bash-4.2$ dirac-dms-filecatalog-cli
   Starting FileCatalog client
   FC:/> cd /skatelescope.eu/user
   
   - Go to the first letter of your user 
   FC:/skatelescope.eu/user>cd c
   
   - Create (mkdir) or go to your user folder
   FC:/skatelescope.eu/user/c>cd cimpan
   
   - Exit File Catalog
   FC:/skatelescope.eu/user/c/cimpan>exit
   bash-4.2$ 
   
   bash-4.2$ /raid/scratch/<your-user>/dirac_ui > dirac-dms-add-file LFN:/skatelescope.eu/user/<first letter of your user>/<your-user>/rascil/RASCIL.img RASCIL.img UKI-NORTHGRID-MAN-HEP-disk
   # UKI-NORTHGRID-MAN-HEP-disk - SE: DIRAC Storage Element

   Then you will find the file RASCIL.img under: 
   FC:/skatelescope.eu/user/<first letter of your user>/<your-user>/rascil/RASCIL.img

Submitting RASCIL job
=====================

.. code:: python

   cat simpleR1.jdl
   JobName    = "InputAndOuputSandbox";
   Executable = "testR1.sh";
   StdOutput = "StdOut";
   StdError = "StdErr";
   InputSandbox = {"testR1.sh"};
   InputData = {"LFN:/skatelescope.eu/user/c/cimpan/rascil/RASCIL-full1.img"};
   OutputSandbox = {"StdOut","StdErr","imaging_dirty.fits","imaging_psf.fits","imaging_restored.fits"};
   OutputSE ="UKI-NORTHGRID-MAN-HEP-disk";
   Site = "LCG.UKI-NORTHGRID-MAN-HEP.uk";

    cat testR1.sh
   #!/bin/bash
   singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C RASCIL-full1.img python3 /rascil/examples/scripts/imaging.py;

Managing RASCIL job
===================

**Details at:**  `Simple_Job <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/CommandLine/index.html>`__

.. code:: python

   $ dirac-wms-job-submit simpleR1.jdl
   JobID = 25260750

   $ dirac-wms-job-status  25260750
   JobID=25260750 Status=Running; MinorStatus=Input Data Resolution; 
   Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

   $ dirac-wms-job-status  25260750
   JobID=25260750 Status=Done; MinorStatus=Execution Complete; 
   Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

Get Output Data RASCIL job
==========================

**Details at:**  `Simple_Job <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/CommandLine/index.html>`__

.. code:: python

   Note: the RASCIL job has 3 image outputs, so we specify them in 
   OutputSandbox and we take the data locally using command

   $ dirac-wms-job-get-output  25260750
   Job output sandbox retrieved in 
   /raid/scratch/<your-user>/dirac_ui/tests/rascilTests/25260750/
   $ cd 25260750
   $ ls
   imaging_dirty.fits  imaging_psf.fits  imaging_restored.fits  StdOut
   $ cat StdOut   #or StdErr

Useful Links

-   `What_is_IRIS <https://www.iris.ac.uk/>`__

-   `GridPP_user-guide <https://github.com/GridPP/user-guides>`__

-   `Getting_on_the_grid <https://github.com/gridpp/user-guides/tree/master/getting-on-the-grid>`__

-   `Grid_user_crash_course <https://www.gridpp.ac.uk/wiki/Grid_user_crash_course>`__

-   `Quick_Guide_to_Dirac <https://www.gridpp.ac.uk/wiki/Quick_Guide_to_Dirac>`__

-   `Getting_started_User_Jobs <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/index.html>`__

-   `Getting_started_Data_Management <https://dirac.readthedocs.io/en/latest/UserGuide/CommandReference/DataManagement/index.html>`__

-   `Getting_started_Command_Line <https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/CommandLine/index.html>`__




:Author: Iulia Cimpan
:Date:   Nov 2021

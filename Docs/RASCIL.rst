===============================================
RASCIL Galahad and IRIS - CL and job submission
===============================================

This documentation follows the steps of the links below:

-   `RASCIL_docker  <https://ska-telescope.gitlab.io/external/rascil/RASCIL_install.html#installation-via-docker>`__

-   `RASCIL_singularity <https://ska-telescope.gitlab.io/external/rascil/installation/RASCIL_docker.html#singularity>`__

-   `RASCIL_gitlab  <https://gitlab.com/ska-telescope/rascil>`__

RASCIL on Galahad and IRIS (CL):
================================

-  Set up environment variables (Galahad) under working directory:

   .. code:: python

      [<your-user>@galahad ~]$ ls /share/nas/<your-user>/
      [<your-user>@galahad ~]$ mkdir /share/nas/<your-user>/.singularity
      [<your-user>@galahad ~]$ export SINGULARITY_CACHEDIR=/share/nas/<youruser>/.singularity

-  Running on existing docker images

   The `RASCIL_Dockerfiles  <https://gitlab.com/ska-telescope/rascil-docker>`__ are in a separate repository.

   The docker images for RASCIL are at:

   .. code:: python

      artefact.skao.int/rascil-base
      artefact.skao.int/rascil-full

   rascil-base does not have the RASCIL test data but is smaller in size. However, for many of the tests and demonstrations the test data is needed, which are       included in rascil-full.

- Run RASCIL with your home directory available inside the image:

 .. code:: python
 
   docker run -it --volume $HOME:$HOME artefact.skao.int/rascil-full
   
- Run an example script 
 
 To run the /rascil/examples/scripts/imaging.py script, we first change directory to the name of the HOME directory, which is the same inside and outside the container, and then give the full address of the script inside the container.   

 .. code:: python
   
   docker run -p 8888:8888 -v $HOME:$HOME -it artefact.skao.int/rascil-full
   rascil@d0c5fc9fc19d:/rascil$ cd /<your home directory>
   rascil@d0c5fc9fc19d:/<your home directory>$ python3 /rascil/examples/scripts/imaging.py
   ...
   rascil@d0c5fc9fc19d:/<your home directory>$ ls -l imaging*.fits
   -rw-r--r-- 1 rascil rascil 2102400 Feb 11 14:04 imaging_dirty.fits
   -rw-r--r-- 1 rascil rascil 2102400 Feb 11 14:04 imaging_psf.fits
   -rw-r--r-- 1 rascil rascil 2102400 Feb 11 14:04 imaging_restored.fits

- RASCIL Notebooks

The docker image to use with RASCIL Jupyter Notebooks is:

 .. code:: python
 
   artefact.skao.int/rascil-notebook
   
   
Run Jupyter Notebooks inside the container:
 
 .. code:: python

   docker run -it -p 8888:8888 --volume $HOME:$HOME artefact.skao.int/rascil-full
   cd /<your home directory>
   jupyter notebook --no-browser --ip 0.0.0.0  /rascil/examples/notebooks/


The Juptyer server will start and output possible URLs to use:

 .. code:: python
 
   [I 14:08:39.041 NotebookApp] Serving notebooks from local directory: /rascil/examples/notebooks
   [I 14:08:39.041 NotebookApp] The Jupyter Notebook is running at:
   [I 14:08:39.042 NotebookApp] http://d0c5fc9fc19d:8888/?token=f050f82ed0f8224e559c2bdd29d4ed0d65a116346bcb5653
   [I 14:08:39.042 NotebookApp]  or http://127.0.0.1:8888/?token=f050f82ed0f8224e559c2bdd29d4ed0d65a116346bcb5653
   [I 14:08:39.042 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
   [W 14:08:39.045 NotebookApp] No web browser found: could not locate runnable browser.


- Images of RASCIL applications

** DOCKER

- Pull the image:

.. code:: python
   
   docker pull artefact.skao.int/rascil-imaging-qa:latest

- Run the image:

.. code:: python

   docker run -v ${PWD}:/myData -e DOCKER_PATH=${PWD} \
    -e CLI_ARGS='--ingest_fitsname_restored /myData/my_restored.fits \
    --ingest_fitsname_residual /myData/my_residual.fits' \
    --rm artefact.skao.int/rascil-imaging-qa:latest



** SINGULARITY

- Pull the image:

.. code:: python

   singularity pull rascil-imaging-qa.img docker://artefact.skao.int/rascil-imaging-qa:latest

- Run the image:

.. code:: python

   singularity run \
    --env CLI_ARGS='--ingest_fitsname_restored test-imaging-pipeline-dask_continuum_imaging_restored.fits \
        --ingest_fitsname_residual test-imaging-pipeline-dask_continuum_imaging_residual.fits' \
    rascil-imaging-qa.img



-  Pull the Rascil image:

   .. code:: python

      [<your-user>@galahad ~]$ singularity pull RASCIL-full.img 
      docker://nexus.engageska-portugal.pt/rascil-docker/rascil-full
      [<your-user>@galahad ~]$ singularity pull RASCIL-base.img 
      docker://nexus.engageska-portugal.pt/rascil-docker/rascil-base

-  Running notebooks

   .. code:: python

      [<your-user>@galahad ~]$ singularity exec RASCIL-full.img jupyter 
      notebook --no-browser --ip 0.0.0.0  /rascil/examples/notebooks/
      [I 10:51:44.514 NotebookApp] Serving notebooks from local directory:
      /rascil/examples/notebooks
      [I 10:51:44.514 NotebookApp] Jupyter Notebook 6.1.4 is running at:
      [I 10:51:44.514 NotebookApp] http://galahad.ast.man.ac.uk:8888/
      ?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102
      [I 10:51:44.514 NotebookApp]  or http://127.0.0.1:8888/
      ?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102
      [I 10:51:44.514 NotebookApp] Use Control-C to stop this server and shut down all
      kernels (twice to skip confirmation).
      [C 10:51:44.519 NotebookApp]

      To access the notebook, open this file in a browser:
          file:///home/<your-user>/.local/share/jupyter/runtime/nbserver-21541-open.html
      Or copy and paste one of these URLs:
          http://galahad.ast.man.ac.uk:8888/
          ?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102
          or http://127.0.0.1:8888/
          ?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102
      [I 10:51:56.498 NotebookApp] 302 GET 
      /?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102 
      (10.242.203.134) 1.04ms


      Access the notebooks on browser using http://galahad.ast.man.ac.uk:8888/
      ?token=26b1523066c7363b5575dde53d5d7780338bf3dc9cbe2102

      Use CTRL <C> to shut down notebook server

-  Running RASCIL as a cluster:

   .. code:: python

      [<your-user>@galahad ~]$ singularity exec RASCIL-full.img 
      python3 /rascil/cluster_tests/ritoy/cluster_test_ritoy.py

      Creating scheduler and 4 workers
      <Client: 'tcp://127.0.0.1:46212' processes=4 threads=4, memory=67.34 GB>
      53870592.0
      *** Successfully reached end in 26.5 seconds ***

      Note: use VNCViewer (see Appendix) to access links on Galahad, like Diagnostics page.

-  Running example script:

   .. code:: python

      [<your-user>@galahad ~]$ singularity exec RASCIL-full.img python3 
      /rascil/examples/scripts/imaging.py

      creates 3 images output
      [<your-user>@galahad ~]$ ls
       imaging_dirty.fits  imaging_psf.fits  imaging_restored.fits

Job submission Galahad
======================

.. code:: python

   [<your-user>@galahad ~]$ cat  slrascil1.sh
   #!/bin/bash
   #SBATCH --ntasks 1
   #SBATCH --time 5:0
   #SBATCH --output=test_%j.log
   pwd; hostname; date

   module load python37base gcc920
   CMD="singularity exec /home/<your-user>/RASCIL-full.img python3 
   /rascil/examples/scripts/imaging.py"
   eval $CMD

   [<your-user>@galahad ~]$  sbatch slrascil1.sh
   Submitted batch job 3404


   [<your-user>@galahad ~]$  squeue
   JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
   3404   CLUSTER slrascil   <your-user>R       0:18      1 compute-0-7

Job submission IRIS
===================

From the server where dirac is installed:

-  start proxy before using any dms commands

   .. code:: python

          bash-4.2$ source bashrc
          bash-4.2$ dirac-proxy-init -g skatelescope.eu_user -M

-  Add the RASCIL container to the filecathalog using command
   "dirac-dms-add-file"

   .. code:: python

      dirac-dms-add-file LFN:/skatelescope.eu/user/c/<your-user>/rascil/RASCIL-full.img  
      RASCIL-full.img  UKI-NORTHGRID-MAN-HEP-disk

-  check where the files has been uploaded using command
   "dirac-dms-filecatalog-cli"

Job submission - submit .jdl 
-----------------------------

-  create .jdl and .sh files

   .. code:: python


      cat simpleR1.jdl
      JobName = "InputAndOuputSandbox";
      Executable = "testR1.sh";
      StdOutput = "StdOut";
      StdError = "StdErr";
      InputSandbox = {"testR1.sh"};
      InputData = {"LFN:/skatelescope.eu/user/c/<your-user>/rascil/RASCIL-full.img"};
      OutputSandbox = {"StdOut","StdErr"};
      OutputData={"imaging_dirty.fits","imaging_psf.fits","imaging_restored.fits"};
      OutputSE ="UKI-NORTHGRID-MAN-HEP-disk";
      Site = "LCG.UKI-NORTHGRID-MAN-HEP.uk";


      cat testR1.sh
      #!/bin/bash
      singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C RASCIL-full.img
      python3 /rascil/examples/scripts/imaging.py;

-  Submit the job

   .. code:: python


      bash-4.2$ dirac-wms-job-submit simpleR1.jdl
      JobID = 25260750

      bash-4.2$ dirac-wms-job-status 25260750
      JobID=25260750 Status=Running; MinorStatus=Input Data Resolution; 
      Site=LCG.UKINORTHGRID-MAN-HEP.uk;

      bash-4.2$ dirac-wms-job-status 25260750
      JobID=25260750 Status=Done; MinorStatus=Execution Complete; 
      Site=LCG.UKINORTHGRID-MAN-HEP.uk;

-  Get output data and output file

   .. code:: python


      bash-4.2$ dirac-wms-job-get-output-data 25336768
      Job 25336768 output data retrieved
      bash-4.2$ ls
      -rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32 imaging_dirty.fits
      -rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32 imaging_psf.fits
      -rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32 imaging_restored.fits

      bash-4.2$ dirac-wms-job-get-output 25336768
      Job output sandbox retrieved in
      /raid/scratch/<your-user>/dirac_ui/tests/rascilTests/ 25336768/
      bash-4.2$ cd 25336768
      bash-4.2$ ls
      StdErr StdOut
      bash-4.2$ cat StdErr
      INFO: Convert SIF file to sandbox...
      INFO: Cleaning up image...

Job submission - submit .py
---------------------------

-  Set up environment variables:

   .. code:: python

         
      #SET THE PATH PYTHON 2.7 INTO $PATH
      #PATH to python 2.7 added
      eg bash-4.2$ export PATH=/usr/local/casa/bin/python:$PATH

-  the job to be submitted and the .sh script

   .. code:: python


      bash-4.2$ cat jobpy.py
      import os
      import sys
      import time
      # setup DIRAC
      from DIRAC.Core.Base import Script
      Script.parseCommandLine(ignoreErrors=False)
      from DIRAC.Interfaces.API.Job import Job
      from DIRAC.Interfaces.API.Dirac import Dirac
      from DIRAC.Core.Security.ProxyInfo import getProxyInfo
      SitesList = ['LCG.UKI-NORTHGRID-MAN-HEP.uk']
      SEList = ['UKI-NORTHGRID-MAN-HEP-disk']
      dirac = Dirac()
      j = Job(stdout='StdOut', stderr='StdErr')
      j.setName('TestJob')
      j.setInputSandbox(["testR1py.sh"])
      j.setInputData(['LFN:/skatelescope.eu/user/c/<your-user>/rascil/RASCILfull.img'])
      j.setOutputSandbox(['StdOut','StdErr'])
      j.setOutputData(['imaging_dirty.fits','imaging_psf.fits','imaging_restored.fits'],
      outputSE='UKI-NORTHGRID-MAN-HEP-disk')
      j.setExecutable('testR1py.sh')
      jobID = dirac.submitJob(j)
      print 'Submission Result: ', jobID


      bash-4.2$ cat testR1py.sh
      #!/bin/bash
      singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C RASCIL-full1.img
      python3 /rascil/examples/scripts/imaging.py

-  Submitting the job

   .. code:: python


      bash-4.2$ python jobpy.py
      Submission Result: {'requireProxyUpload': False, 'OK': True, 'rpcStub':
      (('WorkloadManagement/JobManag er', {'delegatedDN':
      None, 'timeout': 600, 'skipCACheck': False, 'keepAliveLapse': 150,
      'delegatedGroup ': None}), 'submitJob', ('[ \n
      Origin = DIRAC;\n Executable = "$DIRACROOT/scripts/dirac-jobexec";
      \n StdError = StdErr;\n LogLevel = info;\n OutputSE = UKI-NORTHGRIDMAN-
      HEP-disk;\n InputSa ndbox = \n {\n
      "testR1py.sh",\n "SB:GridPPSandboxSE|/SandBox/i/iulia.c.cim
      pan.skatelescope.eu_user/cf8/ca6/cf8ca689995e24c01c068eb6f34126b8.tar.bz2"\n
      };\n JobName = T estJob;\n Priority = 1;\n
      Arguments = "jobDescription.xml -o LogLevel=info";\n JobGroup = skat
      elescope.eu;\n OutputSandbox = \n {\n StdOut,\n
      StdErr,\n Sc ript1_testR1py.sh.log\n
      };\n StdOutput = StdOut;\n InputData = LFN:/skatelescope.eu/user/c
      /<your-user>/rascil/RASCIL-full1.img;\n JobType = User;\n OutputData = \n
      {\n imagin g_dirty.fits,\n
      imaging_psf.fits,\n imaging_restored.fits\n };\n]',)), 'Va
      lue': 25344748, 'JobID': 25344748}

-  Get the results

   .. code:: python


      bash-4.2$ dirac-wms-job-get-output 25344748
      Job output sandbox retrieved in 
      /raid/scratch/<your-user>/dirac_ui/tests/rascilTests/25344748/

      bash-4.2$ cd 25344748
      bash-4.2$ ls
      Script1_testR1py.sh.log StdOut

      bash-4.2$ dirac-wms-job-get-output-data 25344748
      Job 25344748 output data retrieved
      bash-4.2$ ls
      imaging_dirty.fits imaging_psf.fits imaging_restored.fits
      Script1_testR1py.sh.log StdOut

Appendix
========

.. code:: python

   You run vncserver on galahad (already installed). On your windows PC use:
   https://www.tightvnc.com/download-old.php as your vnc viewer.

   When you run vncserver for the first time you will set up a password. 
   It will report it has created a virtual display galahad.ast.man.ac.uk:X
   The X will be a number. You then use that address in your vnc viewer

   [<your-user>@galahad ~]$ vncserver
   [<your-user>@galahad ~]$ vncserver -kill :3
   Killing Xvnc process ID 35841

With vnc I would suggest editing the default .vnc/xstartup file (created
after you run vncserver for the first time) to change the last line to
run /usr/bin/icewm as the window manager rather than xinitrc. You should
then kill off your first vncserver and run it again to pick up the
change. This avoids a bug where sometimes the VNC just displays a black
screen.

.. code:: python


   [<your-user>@galahad ~]$ cat .vnc/xstartup
   #!/bin/shunset SESSION_MANAGER
   unset DBUS_SESSION_BUS_ADDRESS
   #exec /etc/X11/xinit/xinitrc
   /usr/bin/icewm
   [<your-user>@galahad ~]$ vncserver #restarting the server

How to find the host for the for the diagnostics page? It would be
whichever host has started it, so use squeue to see what host is running
your job and then it would be for example http://compute-0-5:8787

.. code:: python

   [<your-user>@galahad ~]$ squeue



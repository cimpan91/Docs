.. contents::
   :depth: 3
..

**RASCIL on command line lofar**

**and IRIS job submission**

**Important links:**

-  https://timcornwell.gitlab.io/rascil/

-  https://timcornwell.gitlab.io/rascil/installation/RASCIL_docker.html#singularity

-  https://github.com/SKA-ScienceDataProcessor/rascil

-  https://gitlab.com/timcornwell/eMERLIN_RASCIL_pipeline

This documentation follows the steps of the link below “Running RASCIL
under docker”

https://timcornwell.gitlab.io/rascil/installation/RASCIL_docker.html but
running it under singularity.

**LOFAR7 command line**

**Set up environment variables:**

**<your-user>@lofar7 /raid/scratch/<your-user> > ./.bash_profile #change
to bash**

'abrt-cli status' timed out

**bash-4.2$ export
SINGULARITY_CACHEDIR=/raid/scratch/<your-user>/cache**

OR

bash-4.2$ export
SINGULARITY_CACHEDIR=/raid/scratch/<your-user>/.singularity

bash-4.2$ TMPDIR=/raid/scratch/<your-user>/tmp

bash-4.2$ mkdir -p $TMPDIR

**Running on existing docker images:**

The singularity containers for RASCIL are on github at:

docker.io/timcornwell/rascil-no-data-no-root

docker.io/timcornwell/rascil-full-no-root

Pull the Rascil image

bash-4.2$ singularity pull RASCIL.img
docker://timcornwell/rascil-no-data-no-root

bash-4.2$ singularity pull RASCIL-full1.img
docker://timcornwell/rascil-full-no-root

Running an example:

bash-4.2$ singularity run RASCIL-full1.img

Singularity> python3 /rascil/examples/scripts/imaging.py

Singularity> ls

RASCIL-full1.img RASCIL.img dask-worker-space imaging_dirty.fits
imaging_psf.fits imaging_restored.fits

**Running notebooks**

Singularity> jupyter notebook --no-browser --ip 0.0.0.0
/rascil/examples/notebooks/

**Running RASCIL as a cluster:**

Singularity> python3 /rascil/cluster_tests/ritoy/cluster_test_ritoy.py

Creating scheduler and 4 workers

<Client: 'tcp://127.0.0.1:42409' processes=4 threads=4, memory=270.18
GB>

53870592.0

\**\* Successfully reached end in 16.5 seconds \**\*

OR from outside the container

bash-4.2$ singularity exec RASCIL-full1.img python3
/rascil/cluster_tests/ritoy/cluster_test_ritoy.py

Creating scheduler and 4 workers

<Client: 'tcp://127.0.0.1:40277' processes=4 threads=4, memory=270.18
GB>

53870592.0

\**\* Successfully reached end in 17.5 seconds \**\*

**IRIS job submission RASCIL**

**bash-4.2$ source bashrc**

bash-4.2$ dirac-proxy-init -g skatelescope.eu_user -M

**1. JDL**

**example 1**

bash-4.2$ dirac-wms-job-submit simpleR1.jdl

JobID = 25260750

bash-4.2$ dirac-wms-job-status 25260750

JobID=25260750 Status=Running; MinorStatus=Input Data Resolution;
Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

bash-4.2$ dirac-wms-job-status 25260750

JobID=25260750 Status=Running; MinorStatus=Application;
Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

bash-4.2$ dirac-wms-job-status 25260750

JobID=25260750 Status=Done; MinorStatus=Execution Complete;
Site=LCG.UKI-NORTHGRID-MAN-HEP.uk;

bash-4.2$

**bash-4.2$ cat simpleR1.jdl**

JobName = "InputAndOuputSandbox";

Executable = "testR1.sh";

StdOutput = "StdOut";

StdError = "StdErr";

InputSandbox = {"testR1.sh"};

InputData =
{"LFN:/skatelescope.eu/user/c/<your-user>/rascil/RASCIL-full1.img"};

OutputSandbox = {"StdOut","StdErr"};

OutputData={"imaging_dirty.fits","imaging_psf.fits","imaging_restored.fits"};

OutputSE ="UKI-NORTHGRID-MAN-HEP-disk";

Site = "LCG.UKI-NORTHGRID-MAN-HEP.uk";

bash-4.2$ cat testR1.sh

#!/bin/bash

singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C RASCIL-full1.img
python3 /rascil/examples/scripts/imaging.py;

bash-4.2$ dirac-wms-job-get-output-data 25336768

Job 25336768 output data retrieved

bash-4.2$ ls

-rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32 imaging_dirty.fits

-rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32 imaging_psf.fits

-rw-r--r--. 1 <your-user> users6 2102400 May 14 17:32
imaging_restored.fits

bash-4.2$ dirac-wms-job-get-output 25336768

Job output sandbox retrieved in
/raid/scratch/<your-user>/dirac_ui/tests/rascilTests/ 25336768/

bash-4.2$ cd 25336768

bash-4.2$ ls

StdErr StdOut

bash-4.2$ cat StdErr

INFO: Convert SIF file to sandbox...

INFO: Cleaning up image...

**JDL**

**example 2 ------ from Willice**

**Note:** 1153+4931.ms.tar contains the calibrated ms and
RascilScriptFor1153.py is the imaging script

cat test.jdl

jobName = "LFNInputSandbox";

Executable = "trial.sh";

StdOutput = "StdOut";

StdError = "StdErr";

Tags = "skatelescope.eu.hmem";

SitesList = "LCG.UKI-NORTHGRID-MAN-HEP.uk";

SEList = "UKI-NORTHGRID-MAN-HEP-disk";

InputSandbox =
{"trial.sh","LFN:/skatelescope.eu/user/w/willice.obonyo/IRIS_RASCIL_test/1153+4931.ms.tar","LFN:/skatelescope.eu/user/w/willice.obonyo/I

RIS_RASCIL_test/RascilScriptFor1153.py","LFN:/skatelescope.eu/user/w/willice.obonyo/IRIS_RASCIL_test/rascil.img"};

OutputSandbox = {"StdOut","StdErr"};

OutputSE = "UKI-NORTHGRID-MAN-HEP-disk";

OutputData = {"StdOut","outputs.tar", "job.info", "*.log","rascil.tar"};

cat trial.sh

#!/bin/bash

echo 'Checking the location of python on the grid';

which python;

echo "==============================================";

echo "Print environment details";

#printenv;

echo "==============================================";

singularity --version;

tar -xzvf 1153+4931.ms.tar

singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C
/cvmfs/sw.skatelescope.eu/images/rascil.img python3
RascilScriptFor1153.py;

tar czf outputs.tar \*.fits

**2.PY**

**Set up environment variables:**

#SET THE PATH PYTHON 2.7 INTO $PATH

#PATH to python 2.7 added

bash-4.2$ export PATH=/usr/local/casa/bin/python:$PATH

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

j.setInputData(['LFN:/skatelescope.eu/user/c/<your-user>/rascil/RASCIL-full1.img'])

j.setOutputSandbox(['StdOut','StdErr'])

j.setOutputData(['imaging_dirty.fits','imaging_psf.fits','imaging_restored.fits'],outputSE='UKI-NORTHGRID-MAN-HEP-disk')

j.setExecutable('testR1py.sh')

jobID = dirac.submitJob(j)

print 'Submission Result: ', jobID

bash-4.2$ cat testR1py.sh

#!/bin/bash

singularity exec --cleanenv -H $PWD:/srv --pwd /srv -C RASCIL-full1.img
python3 /rascil/examples/scripts/imaging.py

bash-4.2$ python jobpy.py

Submission Result: {'requireProxyUpload': False, 'OK': True, 'rpcStub':
(('WorkloadManagement/JobManag er', {'delegatedDN': None, 'timeout':
600, 'skipCACheck': False, 'keepAliveLapse': 150, 'delegatedGroup ':
None}), 'submitJob', ('[ \\n Origin = DIRAC;\n Executable =
"$DIRACROOT/scripts/dirac-jobexec"; \\n StdError = StdErr;\n LogLevel =
info;\n OutputSE = UKI-NORTHGRID-MAN-HEP-disk;\n InputSa ndbox = \\n {\n
"testR1py.sh",\n "SB:GridPPSandboxSE|/SandBox/i/iulia.c.cim
pan.skatelescope.eu_user/cf8/ca6/cf8ca689995e24c01c068eb6f34126b8.tar.bz2"\n
};\n JobName = T estJob;\n Priority = 1;\n Arguments =
"jobDescription.xml -o LogLevel=info";\n JobGroup = skat elescope.eu;\n
OutputSandbox = \\n {\n StdOut,\n StdErr,\n Sc ript1_testR1py.sh.log\n
};\n StdOutput = StdOut;\n InputData = LFN:/skatelescope.eu/user/c
/<your-user>/rascil/RASCIL-full1.img;\n JobType = User;\n OutputData =
\\n {\n imagin g_dirty.fits,\n imaging_psf.fits,\n
imaging_restored.fits\n };\n]',)), 'Va lue': 25344748, 'JobID':
25344748}

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

**Adding file to FC**

<your-user>@lofar7 /raid/scratch/<your-user>/dirac_ui/rascil >
dirac-dms-add-file
LFN:/skatelescope.eu/user/c/<your-user>/rascil/\ **RASCIL-full1.img**
**RASCIL-full1.img** UKI-NORTHGRID-MAN-HEP-disk

Uploading /skatelescope.eu/user/c/<your-user>/rascil/RASCIL-full1.img

Successfully uploaded file to UKI-NORTHGRID-MAN-HEP-disk

<your-user>@lofar7 /raid/scratch/<your-user>/dirac_ui/rascil >

https://dirac.readthedocs.io/en/latest/UserGuide/Tutorials/JDLsAndJobManagementBasic/


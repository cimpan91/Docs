#!/usr/bin/env python
# This script describes the continuum imaging and self-calibration
# for the ALMA LBC SV B6, 1.3mm data on HL Tau. 

# requires CASA 5.1.1-5 or higher. Meant to be run interactively.

#########################################################
# If working from the individual datasets

# Combine the calibrated data from the 9 exections. You might need to
# adjust the path depending on where you've put the calibrated data


interactive=False

#concat(vis=['../Xb2_4/HLTau_Xb2.ms.split.fixed.cal',
#            '../Xc8c_6/HLTau_Xc8c.ms.split.fixed.cal',
#            '../Xdc_10/HLTau_Xdc.ms.split.fixed.cal',
#            '../X33b_11/HLTau_X33b.ms.split.fixed.cal',
#            '../X760_12/HLTau_X760.ms.split.fixed.cal',
#            '../X9dd_13/HLTau_X9dd.ms.split.fixed.cal',
#            '../Xc3c_14/HLTau_Xc3c.ms.split.fixed.cal',
#            '../Xe9b_15/HLTau_Xe9b.ms.split.fixed.cal',
#            '../X387_16/HLTau_X387.ms.split.fixed.cal'],
#       concatvis='HLTau_B6cont.cal')
#
# Channel average data within each spw for speedier cleaning.
# Averaging to 4 channels per spw will allow for nterms=2 cleaning,
# while still provide significant reduction in datasize.

#os.system('rm -rf HLTau_B6cont.calavg')
#split(vis='HLTau_B6cont.cal',
#      outputvis='HLTau_B6cont.calavg',
#      width='32',datacolumn='data')

################################################################
################################################################
# THIS IS THE SCIENCE PORTAL (SP) DATA PRODUCT CALLED "CalibratedData"
# If you have downloaded this product start below this section.
# To go directly to self-calibrated uv-data, run all flagdata
# commands below and using the calibration tables on the SP run
# the final applycal. 
################################################################
################################################################

# list the properties of the combined, averaged data
os.system('rm -rf HLTau_B6cont.calavg.listobs')
listobs(vis='HLTau_B6cont.calavg',listfile='HLTau_B6cont.calavg.listobs')

####################################################################
# Make some uv-plots to better understand the data.

# amplitude vs uv-distance, time-averaging within 5min
os.system('rm -rf HLTau_B6cont.calavg.ampuvdist.png')
plotms(vis='HLTau_B6cont.calavg',coloraxis='spw',yaxis='amp',
       xaxis='uvdist',avgchannel='4',avgtime='300',avgscan=True,
       plotfile='HLTau_B6cont.calavg.ampuvdist.png')

# After the plot finishes Zoom in to shorter baselines 

# some bad data within the spw colored orange (spw=2) is
# immediately visible. Using the "locate" functionality in plotms
# and the listobs, the bad data is due to DV01 in several datasets.

flagdata(vis='HLTau_B6cont.calavg',
         antenna='DV01',spw='2',flagbackup=False)

# click the "reload" toggle and "plot" in plotms to check uv-plot
# after flagging. A couple of other low baselines. Get worst of them.

flagdata('HLTau_B6cont.calavg',
         antenna='DA64&DV14',scan='275,315',flagbackup=False)

# Other things to notice:

# Projected baseline lengths range from 12m to 15.2 km

# comparitive under-density of data from 300-700 m

# Indication of positive spectral index at short baselines (higher
# frequency spws have greater flux than lower frequency). 

plotms(vis='HLTau_B6cont.calavg',coloraxis='spw',
       yaxis='elevation',xaxis='time')

###################################################################
# Image and self-calibrate the data

# Because of the non-optimal antenna configuration for high resolution
# imaging (lots of compact baselines) it is best to use robustness
# that emphasizes more uniform weighting like robust=0. Experiments
# with natural weighting yield a "double-structured" psf with a large
# 1" plateau with a higher resolution (~30mas) core. The results of
# cleaning with a complex psf like this poorly represent the emission
# since the clean process assumes a Guassian restoring beam.

# Because the emission has a wide range of spatial scales we use
# multiscale clean. When using this mode it is very important to make
# a careful mask and clean deeply. Thus the imaging commands below are
# best run interactively, though reasonable stopping thresholds have
# also been given.

# The fractional bandwidth for these B6 data do not technically
# require nterms>1, being near 10% but it is an edge case.

# If you need to restart your self-cal process, un-comment and run the
# following commands:
#
# flagmanager(vis='HLTau_B6cont.calavg',mode='restore',versionname='before_selfcal')
# clearcal('HLTau_B6cont.calavg')
# delmod('HLTau_B6cont.calavg',otf=True)

# Note that in tclean, we *must* set the savemodel parameter, or the
# self-cal step below will not work correctly (because we have not
# saved the clean model in the ms).
# Known issue in tclean in CASA 5.1 + is that the model is not always saved even
# when the parameter 'savemodel' is set. This happens particularly when
# using deconvolver='multiscale' and letting tclean run until the residuals reach 
# the desired threshold, as we are doing here. 
# This will be fixed in the upcoming CASA version 5.3. For now, we will use the following workaround.
# Check the log file for a "Saving model column" statement. If it is missing,
# we need to add in an extra step here to save the model. 

os.system('rm -rf HLTau_B6cont_mscale.*')
tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,niter=30000,threshold='0.1mJy',
       savemodel='modelcolumn')

# Re-run tclean with niter=0,calcres=False,calcpsf=False in order to trigger a 
# 'predict model' step that obeys the savemodel parameter.

tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.1mJy',
       niter=0,calcres=False,calcpsf=False,
       savemodel='modelcolumn')

# beam 35x20 mas

# Below is a description of the interactive clean process followed for
# this initial clean, it need not be followed exactly but is meant to
# be representative of best practices. Since each return to the
# interactive window triggers a major cycle, simply cleaning to the threshold
# with the final mask may not get the same result.

# An initial clean box was made, being a bit conservative in its
# initial extent (see figure) and then 300 iterations were cleaned
# (changing from default max cycleniter 100 in upper left of interactive clean
# window). When the interactive window comes back, check that mask still seems
# reasonable, adjust as needed, and then clean 1000 iterations. Repeat
# check of mask, adjust as needed, clean 3000 iterations. Next clean
# 6000 iterations, followed by 12000 -- it will stop when it gets to
# the residual set by threshold parameter. There is still significant
# emission at this point, but for the first iteration it's best to be
# conservative.

# Next run a self-cal step.
# Start by getting a few solutions per dataset. Each scan is about 70s
# long and there are about 32 scans per dataset over about
# 49m20s. solint='600s' will give 5 solutions per execution.

os.system('rm -rf pcal1')
gaincal(vis='HLTau_B6cont.calavg',caltable='pcal1',gaintype='T',
        refant='DA51',calmode='p',combine='spw',
        solint='600s',minsnr=3.0,minblperant=6)

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',timerange='',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-180,180])

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',timerange='',
        spw='',subplot=111)

# Here we back up the flags in case we would like to restart the self-cal process.
# (you only need to do this step once)

flagmanager(vis='HLTau_B6cont.calavg',mode='save',
            versionname='before_selfcal')

applycal(vis='HLTau_B6cont.calavg',spwmap=[0,0,0,0],
         gaintable=['pcal1'],calwt=False,flagbackup=False)

# Redo imaging plus the extra step to ensure the new model is saved
os.system('rm -rf HLTau_B6cont_mscale_p1.*')
tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_p1',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B6cont_mscale.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=30000,threshold='0.075mJy',
       savemodel='modelcolumn')

tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_p1',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.1mJy',
       niter=0,calcres=False,calcpsf=False,
       savemodel='modelcolumn')

# Iterations set to 1000, 3000, 6000, 6000

# rms=0.015 mJy

# Now try one solution per scan
os.system('rm -rf pcal2')
gaincal(vis='HLTau_B6cont.calavg',caltable='pcal2',gaintype='T',
        refant='DA51',calmode='p',combine='spw',
        solint='inf',minsnr=3.0,minblperant=6)

plotcal(caltable='pcal2',xaxis='time',yaxis='phase',timerange='',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-180,180])

# Because there were quite a number of failed solutions (such that
# data will be flagged when applycal is run), it is best to back the
# flags up so that if you don't like the results of this self-cal
# after imaging, these flags can be restored. This can also be done in
# applycal itself but this way we get to pick the name of the saved
# version.

flagmanager(vis='HLTau_B6cont.calavg',mode='save',
            versionname='before_P2selfcal')

applycal(vis='HLTau_B6cont.calavg',spwmap=[0,0,0,0],spw='',field='',
         gaintable=['pcal2'],gainfield='',calwt=False,flagbackup=True)


os.system('rm -rf HLTau_B6cont_mscale_p2.*')
tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_p2',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B6cont_mscale_p1.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=30000,threshold='0.03mJy',
       savemodel='modelcolumn')

tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_p2',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.1mJy',
       niter=0,calcres=False,calcpsf=False,
       savemodel='modelcolumn')

# Iterations 3000, 6000, 12000,12000

# The integrated flux is about 0.75 Jy

os.system('cp -rf HLTau_B6cont.calavg HLTau_B6cont.calavg.pcal2') 

os.system('rm -rf apcal')
gaincal(vis='HLTau_B6cont.calavg',caltable='apcal',gaintype='T',
        refant='DA51',calmode='a',combine='spw',
        gaintable='pcal2',spwmap=[0,0,0,0],
        solint='600s',minsnr=3.0,minblperant=6)

plotcal(caltable='apcal',xaxis='time',yaxis='amp',timerange='',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,0.6,1.4])

plotcal(caltable='apcal',xaxis='time',yaxis='amp',
        subplot=111,plotrange=[0,0,0.6,1.4])

applycal(vis='HLTau_B6cont.calavg',
         spwmap=[[0,0,0,0],[0,0,0,0]],spw='',field='',
         gaintable=['pcal2','apcal'],gainfield='',calwt=False,flagbackup=True)

plotms(vis='HLTau_B6cont.calavg',coloraxis='spw',yaxis='amp',
       xaxis='uvdist',avgtime='300',avgscan=True, ydatacolumn='corrected')

flagdata(vis='HLTau_B6cont.calavg',scan='263',flagbackup=False)

# Final imaging cycle
os.system('rm -rf HLTau_B6cont_mscale_ap.*')
tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_ap',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B6cont_mscale_p2.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=30000,threshold='0.025mJy',
       savemodel='modelcolumn')

tclean(vis='HLTau_B6cont.calavg',
       imagename='HLTau_B6cont_mscale_ap',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=1600,cell='0.005arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.1mJy',
       niter=0,calcres=False,calcpsf=False,
       savemodel='modelcolumn')

# Produce a final fits image
exportfits('HLTau_B6cont_mscale_ap.image','HLTau_B6cont_mscale_ap.image.fits')








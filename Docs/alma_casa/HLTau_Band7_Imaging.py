#!/usr/bin/env python
# This script describes the continuum imaging and self-calibration
# for the ALMA LBC SV B7, 0.87mm data on HL Tau. 

# requires CASA 5.1.1-5 or higher. Meant to be run interactively.

#########################################################
# If working from the individual datasets

# Combine the calibrated data from the 10 exections. You might need to
# adjust the path depending on where you've put the calibrated data


interactive=False


#os.system('rm -rf HLTau_B7_1_10.tsys.cal')
#concat(vis=['../X20a_1/HLTau_X20a.ms.split.cal',
#            '../X6d8_2/HLTau_X6d8.ms.split.cal',
#            '../Xa16_3/HLTau_Xa16.ms.split.cal',
#            '../X585_4/HLTau_X585.ms.split.cal',
#            '../X826_5/HLTau_X826.ms.split.cal',
#            '../Xacd_6/HLTau_Xacd.ms.split.cal',
#            '../X2e6_7/HLTau_X2e6.ms.split.cal',
#            '../X5ab_8/HLTau_X5ab.ms.split.cal',
#            '../Xab_9/HLTau_Xab.ms.split.cal',
#            '../X446_10/HLTau_X446.ms.split.cal'],
#       concatvis='HLTau_B7cont.cal')

# Channel average data within each spw for speedier cleaning.
# Averaging to 4 channels per spw will allow for nterms=2 cleaning,
# while still provide significant reduction in datasize.

#os.system('rm -rf HLTau_B7cont.calavg')
#split(vis='HLTau_B7cont.cal',
#      outputvis='HLTau_B7cont.calavg',
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
os.system('rm -rf HLTau_B7cont.calavg.listobs')
listobs(vis='HLTau_B7cont.calavg',listfile='HLTau_B7cont.calavg.listobs')

###################################################################
# plot the combined data, look for outliers

# This call may take a few minutes
plotms(vis='HLTau_B7cont.calavg',coloraxis='spw',yaxis='amp',
       xaxis='uvdist',avgtime='300',avgscan=True, avgchannel='4')

plotms(vis='HLTau_B7cont.calavg',coloraxis='spw',
       yaxis='elevation',xaxis='time')


# probably just a timerange with less data than the rest but flagging
# anyway. "Reload" toggle and "plot" after to check result, any other
# outliers.
flagdata(vis='HLTau_B7cont.calavg',flagbackup=False,
          mode='manual',scan='271')

####################################################################
# This self-cal sequence is described with interactive tclean. For
# reference the number of clean iterations done at each return of
# interactive is given. It isn't necessary to follow this exactly but
# at least initially it allows for refinement of the clean mask
# gradually.

os.system('rm -rf HLTau_B7cont_mscale.*')
tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=2048,cell='0.003arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,niter=100000,threshold='0.1mJy',
       savemodel='modelcolumn')

# We may need to add a separate tclean call to force tclean to save
# the clean model for self-calibration. This is a known error that will
# be fixed in the upcoming CASA 5.3 release. 
# If you don't see a line in the logger that says 'Saving model column'
# then please run the command below

tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale',
       specmode='mfs',nterms=1,gridder='standard',
       imsize=2048,cell='0.003arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.1mJy',
       niter=0,calcres=False,calcpsf=False,       
       savemodel='modelcolumn')

# beam 24.0x14.2 mas
# Interactive iterations 300, 1000, 3000, 6000, 12000, 12000

os.system('rm -rf pcal1')
gaincal(vis='HLTau_B7cont.calavg',caltable='pcal1',gaintype='T',
        refant='DA51',calmode='p',combine='spw,scan',
        solint='600s',minsnr=3.0,minblperant=6)

# Since data taken far apart in time, so separate by timerange.

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',
        timerange='<2014/10/31/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',
        timerange='2014/10/31/00:00:00~2014/11/04/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',
        timerange='2014/11/04/00:00:00~2014/11/05/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal1',xaxis='time',yaxis='phase',
        timerange='>2014/11/05/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

# Backup flags before applycal since a fair amount of data will be
# flagged. This will make it easier to fall back if desired.
# See the instructions in the Band 6 HL Tau continuum imaging script for
# how to restart the self-calibration at this point. 

flagmanager(vis='HLTau_B7cont.calavg',mode='save',
            versionname='before_P1selfcal')

applycal(vis='HLTau_B7cont.calavg',spwmap=[0,0,0,0],spw='',field='',
         gaintable=['pcal1'],gainfield='',calwt=False,flagbackup=False)

os.system('rm -rf HLTau_B7cont_mscale_p1.*')
tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale_p1',
       specmode='mfs',gridder='standard',
       imsize=2048,cell='0.0035arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B7cont_mscale.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=100000,threshold='0.075mJy',
       savemodel='modelcolumn')

# Again, if the logger does not state that it is saving the model, run
# tclean again with niter=0, mask='', calcres=False, calcpsf=False:

tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale_p1',
       specmode='mfs',gridder='standard',
       imsize=2048,cell='0.0035arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.075mJy',
       niter=0,calcres=False,calcpsf=False,       
       savemodel='modelcolumn')

# beam 24.9x15.6
# Interactive iterations 6000, 12000, 12000, 12000, 12000
# rms 0.022 mJy/beam

# One solution per scan was attempted but there are many failed
# solutions, most of them for intermediate or long baseline antennas.
os.system('rm -rf pcal2')
gaincal(vis='HLTau_B7cont.calavg',caltable='pcal2',gaintype='T',
        refant='DA51',calmode='p',combine='spw,scan',
        solint='180s',minsnr=3.0,minblperant=6)

plotcal(caltable='pcal2',xaxis='time',yaxis='phase',
        timerange='<2014/10/31/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal2',xaxis='time',yaxis='phase',
        timerange='2014/10/31/00:00:00~2014/11/04/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal2',xaxis='time',yaxis='phase',
        timerange='2014/11/04/00:00:00~2014/11/05/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])

plotcal(caltable='pcal2',xaxis='time',yaxis='phase',
        timerange='>2014/11/05/00:00:00',
        spw='',iteration='antenna',subplot=411,plotrange=[0,0,-80,80])


flagmanager(vis='HLTau_B7cont.calavg',mode='save',
            versionname='before_P2selfcal')

applycal(vis='HLTau_B7cont.calavg',spwmap=[0,0,0,0],spw='',field='',
         gaintable=['pcal2'],gainfield='',calwt=False,flagbackup=False)

os.system('rm -rf HLTau_B7cont_mscale_p2.*')
tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale_p2',
       specmode='mfs',gridder='standard',
       imsize=2048,cell='0.0035arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B7cont_mscale_p1.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=100000,threshold='0.06mJy',
       savemodel='modelcolumn')

# Again, if the logger does not state that it is saving the model, run
# tclean again with niter=0, mask='', calcres=False, calcpsf=False:

tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale_p2',
       specmode='mfs',gridder='standard',
       imsize=2048,cell='0.0035arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='',
       weighting='briggs',robust=0.0,
       interactive=False,threshold='0.06mJy',
       niter=0,calcres=False,calcpsf=False,       
       savemodel='modelcolumn')


# Beam 29x18.7 mas
# Interactive iterations 12000, 12000


# note, attempts to use shorter solint result in lots of flagged data.
os.system('rm -rf apcal')
gaincal(vis='HLTau_B7cont.calavg',caltable='apcal',gaintype='T',
        refant='DA51',calmode='a',combine='spw,scan',
        gaintable='pcal2',spwmap=[0,0,0,0],
        solint='inf',minsnr=3.0,minblperant=6)


plotcal(caltable='apcal',xaxis='time',yaxis='amp',timerange='',
        spw='',iteration='antenna',subplot=421)

plotcal(caltable='apcal',xaxis='time',yaxis='amp',timerange='',
        spw='',subplot=111)

# backup data before applying amplitude
os.system('cp -r HLTau_B7cont.calavg HLTau_B7cont.calavg.pcal2')

applycal(vis='HLTau_B7cont.calavg',spwmap=[[0,0,0,0],[0,0,0,0]],
         gaintable=['pcal2','apcal'],gainfield='',calwt=False,flagbackup=True)

# Check to make sure that none of the amplitude solutions have
# gone wacky.
plotms(vis='HLTau_B7cont.calavg',coloraxis='spw',yaxis='amp',
       xaxis='uvdist',avgtime='100',avgchannel='4',ydatacolumn='corrected')

# Final clean including primary beam correction
# Primary-beam corrected image will have .image.pbcor file extension
os.system('rm -rf HLTau_B7cont_mscale_ap.*')
tclean(vis='HLTau_B7cont.calavg',
       imagename='HLTau_B7cont_mscale_ap',
       specmode='mfs',gridder='standard',
       imsize=2048,cell='0.0035arcsec',
       deconvolver='multiscale',scales=[0,5,15],
       mask='HLTau_B7cont_mscale_p2.mask',
       weighting='briggs',robust=0.0,
       interactive=False,niter=100000,threshold='0.05mJy',
       pbcor=True,pblimit=0.3,
       savemodel='modelcolumn')

# 30.0x19.0 mas
# Interactive iterations 12000, 12000, 12000, 12000, 12000, 12000, 12000

# If we didn't set pbcor=True in the previous tclean call, we could create
# the primary beam corrected image using impbcor instead:
os.system('rm -rf HLTau_B7cont_mscale_ap.image.pbcor')
impbcor(imagename='HLTau_B7cont_mscale_ap.image',
        pbimage='HLTau_B7cont_mscale_ap.pb',
        outfile='HLTau_B7cont_mscale_ap.image.pbcor',
        cutoff=0.3)

exportfits('HLTau_B7cont_mscale_ap.image.pbcor',
           'HLTau_B7cont_mscale_ap.image.pbcor.fits')


#!/usr/bin/env python
# This script describes the imaging for the ALMA LBC SV B6 data on Mira
# Requires CASA 4.2.2 or higher. Meant to be run interactively.

###################################################################
# If working from the individual datasets
# Concatenate the data and split off the continuum

# Note the positions differ by a small amount, particularly in Dec (0.002")
# Should not significantly affect measurements, but requires DIRTOL to combine
# Will not combine spws, resulting in 12

interactive=False


#os.system('rm -rf Mira_2days.ms.split.concat')
#concat(vis=['Mira_X423.ms.split.cal','Mira_X137.ms.split.cal'],
#    dirtol='0.01arcsec',
#    concatvis='Mira_2days.ms.split.concat')

# Split off the continuum, averaging in frequency
#os.system('rm -rf Mira_2days.ms.split.calavg')
#split(vis='Mira_2days.ms.split.concat',
#    outputvis='Mira_2days.ms.split.calavg',
#    width=16,spw='0,7',datacolumn='data')



###################################################################
###################################################################
# THESE TWO MS FILES ARE CONTAINED IN THE SCIENCE PORTAL (SP) DATA 
# PRODUCT CALLED "CalibratedData". If you have downloaded these 
# products, start below this section for imaging. 
###################################################################
###################################################################


###################################################################
# Continuum imaging

# Examine the data. For e.g.:
plotms(vis='Mira_2days.ms.split.calavg',coloraxis='spw',yaxis='amp',
    xaxis='uvdist',avgtime='60')

# Create a first-order cleaned image, defining the mask interactively
os.system('rm -rf Mira_2days.cont.*')
clean(vis='Mira_2days.ms.split.calavg',
    imagename='Mira_2days.cont',
    spw='',field='',
    mode='mfs',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# First round of phase-only self-cal
os.system('rm -rf cont_2days_pcal1')
gaincal(vis='Mira_2days.ms.split.calavg',
    caltable='cont_2days_pcal1',gaintype='T',
    refant='DV04',calmode='p',combine='',
    solint='inf',minsnr=3.0,minblperant=6)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='cont_2days_pcal1',xaxis='time',yaxis='phase',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,-80,80])

# Apply the solutions
applycal(vis='Mira_2days.ms.split.calavg',spwmap=[],spw='',field='',
    gaintable=['cont_2days_pcal1'],calwt=False,flagbackup=False)

# Create a new cleaned image
os.system('rm -rf Mira_2days.cont_p1.*')
clean(vis='Mira_2days.ms.split.calavg',
    imagename='Mira_2days.cont_p1',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='Mira_2days.cont.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# Second round of phase-only self-cal
os.system('rm -rf cont_2days_pcal2')
gaincal(vis='Mira_2days.ms.split.calavg',caltable='cont_2days_pcal2',
    gaintype='T',refant='DV04',calmode='p',combine='',
    solint='12s',minsnr=3.0,minblperant=6)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='cont_2days_pcal2',xaxis='time',yaxis='phase',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,-180,180])

# Apply the solutions
applycal(vis='Mira_2days.ms.split.calavg',spwmap=[],spw='',field='',
    gaintable=['cont_2days_pcal2'],calwt=False,flagbackup=False)

# Create a new cleaned image
os.system('rm -rf Mira_2days.cont_p2.*')
clean(vis='Mira_2days.ms.split.calavg',
    imagename='Mira_2days.cont_p2',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='Mira_2days.cont_p1.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# Do a round of amplitude+phase self-cal
# Note that setting combine='spw' has no effect in this case because the spws
# are also separated in time. If it is used, as in this case, the spwmap
# parameter in the corresponding applycal command should be changed accordingly 
# (as in the example below). 
os.system('rm -rf cont_2days_apcal')
gaincal(vis='Mira_2days.ms.split.calavg',caltable='cont_2days_apcal',
    gaintype='T',refant='DV04',calmode='ap',combine='spw,scan',
    solint='300s',minsnr=3.0,minblperant=6,
    gaintable='cont_2days_pcal2',spwmap=[],solnorm=True)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='cont_2days_apcal',xaxis='time',yaxis='amp',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,0.4,1.6])

plotcal(caltable='cont_2days_apcal',xaxis='time',yaxis='amp',timerange='',
    spw='',iteration='',subplot=111,plotrange=[0,0,0.8,1.2])

# Apply the solutions
applycal(vis='Mira_2days.ms.split.calavg',spwmap=[[0,1],[0,0]],
    gaintable=['cont_2days_pcal2','cont_2days_apcal'],calwt=False,flagbackup=False)

# Create the final cleaned image
os.system('rm -rf Mira_2days.cont_ap.*')
clean(vis='Mira_2days.ms.split.calavg',
    imagename='Mira_2days.cont_ap',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='Mira_2days.cont_p2.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.05mJy')

###################################################################
# BAND 6 continuum subtraction

# RRL 30a    spw='6' '231.90093GHz'
# H2O v=1    spw='5' '232.68670GHz'
# SiO v=0    spw='4' '217.10498GHz'
# SiO v=1    spw='3' '215.59595GHz'
# SiO v=2    spw='2' '214.08854GHz'
# 29SiO v=0  spw='1' '214.38576GHz'

# Examine the data
plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='1,8',avgtime='1e8',avgscan=True,
    transform=True,restfreq='214.38576GHz',freqframe='LSRK')

plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='2,9',avgtime='1e8',avgscan=True,
    transform=True,restfreq='214.08854GHz',freqframe='LSRK')

plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='3,10',avgtime='1e8',avgscan=True,
    transform=True,restfreq='215.59595GHz',freqframe='LSRK')

plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='4,11',avgtime='1e8',avgscan=True,
    transform=True,restfreq='217.10498GHz',freqframe='LSRK')

plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='5,12',avgtime='1e8',avgscan=True,
    transform=True,restfreq='232.68670GHz',freqframe='LSRK')

plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='velocity',
    spw='6,13',avgtime='1e8',avgscan=True,
    transform=True,restfreq='231.90093GHz',freqframe='LSRK')

# Determine the continuum-only channels
plotms(vis='Mira_2days.ms.split.concat',yaxis='amp',xaxis='channel',
    spw='',avgtime='1e8',avgscan=True,iteraxis='spw')
# The continuum channels are:
# spws 0 and 7:7~120
# spws 1 and 8:0~300;600~950
# spws 2 and 9:0~300;600~950
# spws 3 and 10:0~300;600~950
# spws 4 and 11:0~300;600~950
# spws 5 and 12:0~800;1400~1900
# spws 6 and 13:0~1900

# Do the continuum subtraction
# The 'invalid source ID' warnings are not relevant and can be safely ignored.
# Note that again, setting combine='spw' has no effect in this case, as the 
# spws are also separated in time. If it is used, as in this case, the spwmap
# parameter in the corresponding applycal command should be changed accordingly 
# (as in the example below). 
fitspw='0:7~120,1~4:10~300;600~950,5:10~800;1400~1900,6:10~1900,7:7~120,8~11:10~300;600~950,12:10~800;1400~1900,13:10~1900'
os.system('rm -rf Mira_2days.ms.split.concat.contsub')
uvcontsub(vis='Mira_2days.ms.split.concat',
    fitspw=fitspw,combine='spw',fitorder=1)


###################################################################
# Line self-calibration using the strong SiOv1 emission

# Identify channels with peak SiOv1 line emission
plotms(vis='Mira_2days.ms.split.concat.contsub',yaxis='amp',xaxis='channel',
    spw='3,10',avgtime='1e8',avgscan=True,coloraxis='spw')

# Split off these channels
os.system('rm -rf SiOv1_2days_chan.ms')
split(vis='Mira_2days.ms.split.concat.contsub',
    spw='3:491~492,10:491~492',width=2,
    outputvis='SiOv1_2days_chan.ms',datacolumn='data')

# Create a first order cleaned image, defining the mask interactively
os.system('rm -rf SiOv1_2days_chan_0.*')
clean(vis='SiOv1_2days_chan.ms',
    imagename='SiOv1_2days_chan_0',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# Do a round of phase-only self-cal
os.system('rm -rf sio_2days_pcal1')
gaincal(vis='SiOv1_2days_chan.ms',caltable='sio_2days_pcal1',gaintype='T',
    refant='DV04',calmode='p',combine='spw',
    solint='inf',minsnr=3.0,minblperant=6)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='sio_2days_pcal1',xaxis='time',yaxis='phase',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,-80,80])

# Apply the solutions
applycal(vis='SiOv1_2days_chan.ms',spwmap=[0,0],spw='',field='',
    gaintable=['sio_2days_pcal1'],calwt=False,flagbackup=False)

# Create a new cleaned image
os.system('rm -rf SiOv1_2days_chan_p1.*')
clean(vis='SiOv1_2days_chan.ms',
    imagename='SiOv1_2days_chan_p1',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='SiOv1_2days_chan_0.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# Do a second round of phase-only self-cal
os.system('rm -rf sio_2days_pcal2')
gaincal(vis='SiOv1_2days_chan.ms',caltable='sio_2days_pcal2',gaintype='T',
    refant='DV04',calmode='p',combine='spw',
    solint='int',minsnr=3.0,minblperant=6)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='sio_2days_pcal2',xaxis='time',yaxis='phase',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,-180,180])

# Apply the solutions
applycal(vis='SiOv1_2days_chan.ms',spwmap=[0,0],spw='',field='',
    gaintable=['sio_2days_pcal2'],calwt=False,flagbackup=False)

# Create a new cleaned image
os.system('rm -rf SiOv1_2days_chan_p2.*')
clean(vis='SiOv1_2days_chan.ms',
    imagename='SiOv1_2days_chan_p2',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='SiOv1_2days_chan_p1.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

# Do a round of amplitude+phase self-cal
os.system('rm -rf sio_2days_apcal')
gaincal(vis='SiOv1_2days_chan.ms',caltable='sio_2days_apcal',gaintype='T',
    refant='DV04',calmode='ap',combine='spw',
    solint='inf',minsnr=3.0,minblperant=6,
    gaintable='sio_2days_pcal2',spwmap=[0,0],solnorm=True)

# Examine the solutions, flagging any obvious problems
plotcal(caltable='sio_2days_apcal',xaxis='time',yaxis='amp',timerange='',
    spw='',iteration='antenna',subplot=421,plotrange=[0,0,0.4,1.6])

plotcal(caltable='sio_2days_apcal',xaxis='time',yaxis='amp',timerange='',
    spw='',iteration='',subplot=111,plotrange=[0,0,0.8,1.2])

#Apply the solutions
applycal(vis='SiOv1_2days_chan.ms',spwmap=[[0,0],[0,0]],
    gaintable=['sio_2days_pcal2','sio_2days_apcal'],calwt=False,flagbackup=False)

# Create the final cleaned image
os.system('rm -rf SiOv1_2days_chan_ap.*')
clean(vis='SiOv1_2days_chan.ms',
    imagename='SiOv1_2days_chan_ap',
    spw='',field='',
    mode='mfs',nterms=1,imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    interactive=False,
    mask='SiOv1_2days_chan_p2.mask',
    weighting='briggs',robust=0.5,
    niter=10000,threshold='0.1mJy')

###################################################################
# Create image cubes

# Apply the self-cal solutions determined above using SiOv1 to the 
# continuum-subtracted data
applycal(vis='Mira_2days.ms.split.concat.contsub',
    spwmap=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    gaintable=['sio_2days_pcal2','sio_2days_apcal'],calwt=False,flagbackup=False)

# Now create the image cubes, using multiscale cleaning for the cubes showing
# more extended line emission

# Create the SiOv0 cube, defining the mask interactively
os.system('rm -rf Mira_2days.SiOv0_apms.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.SiOv0_apms',
    spw='4,11',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='217.10498GHz',
    interactive=False,multiscale=[0,5,15],
    mask='',
    weighting='briggs',robust=1.0,
    niter=100000,threshold='0.1mJy')

# Create the SiOv1 cube, defining the mask interactively
os.system('rm -rf Mira_2days.SiOv1_apms.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.SiOv1_apms',
    spw='3,10',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='215.59595GHz',
    interactive=False,multiscale=[0,5,15],
    mask='',
    weighting='briggs',robust=1.0,
    niter=100000,threshold='0.1mJy')

# Create the 29SiOv0 cube, defining the mask interactively
os.system('rm -rf Mira_2days.29SiOv0_apms.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.29SiOv0_apms',
    spw='1,8',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='214.38576GHz',
    interactive=False,multiscale=[0,5,15],
    mask='',
    weighting='briggs',robust=1.0,
    niter=100000,threshold='0.1mJy')

# Create the H20v1 cube, defining the mask interactively
os.system('rm -rf Mira_2days.H2Ov1_ap.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.H2Ov1_ap',
    spw='5,12',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='232.68670GHz',
    interactive=False,
    mask='',
    weighting='briggs',robust=1.0,
    niter=100000,threshold='0.1mJy')

# Create the SiOv2 cube, defining the mask interactively
os.system('rm -rf Mira_2days.SiOv2_ap.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.SiOv2_ap',
    spw='2,9',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='214.08854GHz',
    interactive=False,
    mask='',
    weighting='briggs',robust=1.0,
    niter=100000,threshold='0.1mJy')

# Create the H30 cube. Note there is no detection here
os.system('rm -rf Mira_2days.H30_ap.*')
clean(vis='Mira_2days.ms.split.concat.contsub',
    imagename='Mira_2days.H30_ap',
    spw='6,13',
    mode='velocity',imagermode='csclean',
    imsize=640,cell='0.005arcsec',
    start='30km/s',width='0.4km/s',nchan=85,
    outframe='LSRK',restfreq='231.90093GHz',
    interactive=False,
    mask='',
    weighting='briggs',robust=1.0,
    niter=0,threshold='0.1mJy')


###################################################################
# Create the 0th moment maps

immoments(imagename='Mira_2days.SiOv0_apms.image',
    chans='16~73',moments=[0],
    outfile='Mira_2days.SiOv0_apms.image.mom0')

immoments(imagename='Mira_2days.29SiOv0_apms.image',
    chans='16~73',moments=[0],
    outfile='Mira_2days.29SiOv0_apms.image.mom0')

immoments(imagename='Mira_2days.SiOv1_apms.image',
    chans='16~73',moments=[0],
    outfile='Mira_2days.SiOv1_apms.image.mom0')

immoments(imagename='Mira_2days.SiOv2_ap.image',
    chans='16~73',moments=[0],
    outfile='Mira_2days.SiOv2_ap.image.mom0')

immoments(imagename='Mira_2days.H2Ov1_ap.image',
    chans='16~73',moments=[0],
    outfile='Mira_2days.H2Ov1_ap.image.mom0')

exportfits(imagename='Mira_2days.29SiOv0_apms.image.mom0', fitsimage='Mira_2days.29SiOv0_apms.image.mom0.fits')
exportfits(imagename='Mira_2days.SiOv2_ap.image.mom0', fitsimage='Mira_2days.SiOv2_ap.image.mom0.fits')
exportfits(imagename='Mira_2days.H2Ov1_ap.image.mom0', fitsimage='Mira_2days.H2Ov1_ap.image.mom0.fits')
exportfits(imagename='Mira_2days.SiOv0_apms.image.mom0', fitsimage='Mira_2days.SiOv0_apms.image.mom0.fits')
exportfits(imagename='Mira_2days.SiOv1_apms.image.mom0', fitsimage='Mira_2days.SiOv1_apms.image.mom0.fits')

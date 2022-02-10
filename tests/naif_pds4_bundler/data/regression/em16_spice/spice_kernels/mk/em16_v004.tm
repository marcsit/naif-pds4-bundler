KPL/MK

Meta-kernel for ExoMars 2016 Archived Kernels
==========================================================================

   This meta-kernel lists the ExoMars 2016 Archived SPICE kernels
   providing information for the full mission. All of the kernels listed
   below are archived in the PSA ExoMars 2016 SPICE kernel archive.

   This set of files and the order in which they are listed were picked to
   provide the best available data and the most complete coverage for the
   specified year based on the information about the kernels available at
   the time this meta-kernel was made. For detailed information about the
   kernels listed below refer to the internal comments included in the
   kernels and the documentation accompanying the ExoMars 2016
   SPICE kernel archive.


Usage of the Meta-kernel
-------------------------------------------------------------------------

   This file is used by the SPICE system as follows: programs that make
   use of this kernel must "load" the kernel normally during program
   initialization. Loading the kernel associates the data items with
   their names in a data structure called the "kernel pool".
   The SPICELIB routine FURNSH loads a kernel into the pool.


Implementation Notes
-------------------------------------------------------------------------

   It is recommended that users make a local copy of this file and
   modify the value of the PATH_VALUES keyword to point to the actual
   location of the ExoMars 2016 SPICE data set's ``data'' directory
   on their system. Replacing ``/'' with ``\'' and converting line
   terminators to the format native to the user's system may also be
   required if this meta-kernel is to be used on a non-UNIX workstation.


-------------------

   This file was created on 2022-01-31 by Alfredo Escalante Lopez ESA/ESAC.
   The original name of this file was em16_v004.tm.


   \begindata

     PATH_VALUES       = ( '..' )

     PATH_SYMBOLS      = ( 'KERNELS' )

     KERNELS_TO_LOAD   = (

'$KERNELS/ck/em16_tgo_acs_scm_20160314_20161101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_acs_spm_20161101_20170301_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_acs_sam_20170301_20180311_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_acs_ssm_20180311_20190101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_acs_ssm_20190101_20200101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_acs_ssm_20200101_20210101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_scm_20160404_20161121_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_spm_20161121_20170302_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_sam_20170301_20180314_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_ssm_20180314_20190101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_ssm_20190101_20200101_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_nomad_ssm_20200101_20201231_s20210611_v01.bc'
'$KERNELS/ck/em16_tgo_hga_scm_20160315_20161101_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_hga_spm_20161101_20170301_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_hga_sam_20170301_20180312_s20190703_v01.bc'
'$KERNELS/ck/em16_tgo_hga_ssm_20180311_20190101_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_hga_ssm_20190101_20200101_s20191109_v02.bc'
'$KERNELS/ck/em16_tgo_hga_ssm_20200101_20210101_s20210113_v03.bc'
'$KERNELS/ck/em16_tgo_hga_ssm_20210101_20220101_s20220103_v01.bc'
'$KERNELS/ck/em16_tgo_sa_scm_20160315_20161101_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_sa_spm_20161101_20170301_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_sa_sam_20170301_20180312_s20190703_v01.bc'
'$KERNELS/ck/em16_tgo_sa_ssm_20180311_20190101_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_sa_ssm_20190101_20200101_s20191109_v02.bc'
'$KERNELS/ck/em16_tgo_sa_ssm_20200101_20210101_s20210113_v03.bc'
'$KERNELS/ck/em16_tgo_sa_ssm_20210101_20220101_s20220103_v01.bc'
'$KERNELS/ck/em16_tgo_sc_fpp_014_01_20160314_20170315_s20170201_v01.bc'
'$KERNELS/ck/em16_tgo_sc_fsp_210_01_20180222_20220115_s20211209_v01.bc'
'$KERNELS/ck/em16_tgo_sc_scm_20160315_20161101_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_sc_spm_20161101_20170301_s20191109_v01.bc'
'$KERNELS/ck/em16_tgo_sc_sam_20170301_20180312_s20190703_v01.bc'
'$KERNELS/ck/em16_tgo_sc_ssm_20180311_20190101_s20191109_v02.bc'
'$KERNELS/ck/em16_tgo_sc_ssm_20190101_20200101_s20191109_v02.bc'
'$KERNELS/ck/em16_tgo_sc_ssm_20200101_20210101_s20210113_v03.bc'
'$KERNELS/ck/em16_tgo_sc_ssm_20210101_20220101_s20220103_v01.bc'

'$KERNELS/fk/em16_tgo_v24.tf'
'$KERNELS/fk/em16_tgo_ops_v03.tf'
'$KERNELS/fk/em16_dsk_surfaces_v03.tf'
'$KERNELS/fk/rssd0002.tf'
'$KERNELS/fk/earth_topo_050714.tf'
'$KERNELS/fk/earthfixeditrf93.tf'
'$KERNELS/fk/estrack_v04.tf'
'$KERNELS/fk/earthstns_ru_20210706.tf'
'$KERNELS/fk/em16_tgo_relay_locations_v02.tf'

'$KERNELS/ik/em16_tgo_acs_v08.ti'
'$KERNELS/ik/em16_tgo_cassis_v08.ti'
'$KERNELS/ik/em16_tgo_frend_v06.ti'
'$KERNELS/ik/em16_tgo_nomad_v04.ti'
'$KERNELS/ik/em16_tgo_str_v03.ti'

'$KERNELS/lsk/naif0012.tls'

'$KERNELS/pck/pck00010.tpc'
'$KERNELS/pck/de-403-masses.tpc'

'$KERNELS/sclk/em16_tgo_step_20220103.tsc'

'$KERNELS/spk/em16_tgo_struct_v05.bsp'
'$KERNELS/spk/em16_tgo_cog_000_20160314_20300101_v01.bsp'
'$KERNELS/spk/em16_tgo_cog_210_01_20180220_20220115_v01.bsp'
'$KERNELS/spk/em16_tgo_fsp_048_01_20160314_20181231_v03.bsp'
'$KERNELS/spk/em16_tgo_fsp_065_01_20181120_20190429_v03.bsp'
'$KERNELS/spk/em16_tgo_fsp_080_01_20190305_20190817_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_082_01_20190318_20190903_v03.bsp'
'$KERNELS/spk/em16_tgo_fsp_099_01_20190716_20191228_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_114_01_20191024_20200411_v01.bsp'
'$KERNELS/spk/em16_tgo_fsp_116_01_20191111_20200425_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_133_01_20200309_20200822_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_150_01_20200706_20201219_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_167_01_20201102_20210417_v02.bsp'
'$KERNELS/spk/em16_tgo_fsp_181_01_20210209_20210724_v01.bsp'
'$KERNELS/spk/em16_tgo_fsp_184_01_20210301_20211002_v01.bsp'
'$KERNELS/spk/em16_tgo_fsp_201_01_20210628_20211211_v01.bsp'
'$KERNELS/spk/em16_tgo_fsp_210_01_20210830_20220212_v01.bsp'
'$KERNELS/spk/de432s.bsp'
'$KERNELS/spk/mar097_20160314_20300101.bsp'
'$KERNELS/spk/outerplanets_v0004.bsp'
'$KERNELS/spk/earthstns_itrf93_050714.bsp'
'$KERNELS/spk/estrack_v04.bsp'
'$KERNELS/spk/earthstns_ru_20210706.bsp'
'$KERNELS/spk/em16_tgo_relay_locations_v02.bsp'

                         )

   \begintext


Contact Information
------------------------------------------------------------------------

   If you have any questions regarding this file contact the
   ESA SPICE Service at ESAC:

           Alfredo Escalante Lopez
           (+34) 91 813 14 29
           spice@sciops.esa.int

   or NAIF at JPL:

           Marc Costa Sitja
           +1 (818) 354-4852
           Marc.Costa.Sitja@jpl.nasa.gov


End of MK file.

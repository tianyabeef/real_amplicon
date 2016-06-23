#set anaconda2
export PATH=/data_center_03/USER/huangy/soft/MAIN/anaconda2/bin:$PATH
# User install R software
export LD_LIBRARY_PATH=/home/huangy/lib/lib:/home/huangy/lib/lib/pcre:/data_center_03/USER/huangy/soft/MAIN/anaconda2/lib/:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=/home/huangy/lib/include:/usr/include/libxml2:/data_center_03/USER/huangy/soft/MAIN/anaconda2/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/home/huangy/lib/include:/usr/include/libxml2:/data_center_03/USER/huangy/soft/MAIN/anaconda2/include:$CPLUS_INCLUDE_PATH
export OBJC_INCLUDE_PATH=/home/huangy/lib/include:/usr/include/libxml2:/data_center_03/USER/huangy/soft/MAIN/anaconda2/include/:$OBJC_INCLUDE_PATH
export LIBRARY_PATH=/home/huangy/lib/lib:/data_center_03/USER/huangy/soft/MAIN/anaconda2/lib/:$LIBRARY_PATH
export PKG_CONFIG_PATH=/home/huangy/lib/lib/pkgconfig:$PKG_CONFIG_PATH

# set R
R_HOME=/data_center_03/USER/huangy/soft/MAIN/R-3.3.0
export PATH=$R_HOME/bin:$PATH
export R_LIBS=$R_HOME/library
export LD_LIBRARY_PATH=$R_HOME/lib:$R_HOME/lib64/R/lib/:$LD_LIBRARY_PATH

KronaTools_PATH=/data_center_07/User/liangzb/soft/KronaTools/KronaTools-2.6/bin
export PATH=$KronaTools_PATH:$PATH

Mafft_PATH=/data_center_03/USER/huangy/soft/mafft-7.245-without-extensions/bin
export PATH=$Mafft_PATH:$PATH

LEfSe_PATH=/data_center_03/USER/huangy/soft/LEfSe_lzb/
export PATH=$LEfSe_PATH:$PATH


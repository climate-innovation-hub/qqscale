# Quantile delta change: precipitation

HIST_VAR=pr
REF_VAR=precip
TARGET_VAR=pr
HIST_UNITS="kg m-2 s-1"
TARGET_UNITS="kg m-2 s-1"
REF_UNITS="mm d-1"
OUTPUT_UNITS="mm d-1"
OUTPUT_GRID=adjustment

MAPPING=qdm
SCALING=multiplicative
GROUPING=monthly
MODEL=ACCESS-ESM1-5
OBS_DATASET=AGCD
EXPERIMENT=ssp370
RUN=r1i1p1f1
HIST_START=1995
HIST_END=2014
TARGET_START=2035
TARGET_END=2064
REF_START=1995
REF_END=2014
# (Hobart)
#EXAMPLE_LAT = -42.9
#EXAMPLE_LON = 147.3
# (Alice Springs)
#EXAMPLE_LAT = -23.7
#EXAMPLE_LON = 133.88
# (Townsville)
EXAMPLE_LAT = -19.26
EXAMPLE_LON = 146.8
EXAMPLE_MONTH = 5

HIST_FILES := /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/day/pr/gn/latest/pr_day_ACCESS-ESM1-5_historical_r1i1p1f1_gn_19500101-19991231.nc /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/day/pr/gn/latest/pr_day_ACCESS-ESM1-5_historical_r1i1p1f1_gn_20000101-20141231.nc
HIST_SSR_FILE = pr-ssr_day_ACCESS-ESM1-5_historical_r1i1p1f1_gn_${HIST_START}0101-${HIST_END}1231.nc

TARGET_FILES := /g/data/fs38/publications/CMIP6/ScenarioMIP/CSIRO/ACCESS-ESM1-5/ssp370/r1i1p1f1/day/pr/gn/latest/pr_day_ACCESS-ESM1-5_ssp370_r1i1p1f1_gn_20150101-20641231.nc
TARGET_SSR_FILE = pr-ssr_day_ACCESS-ESM1-5_ssp370_r1i1p1f1_gn_${TARGET_START}0101-${TARGET_END}1231.nc

REF_FILES := /g/data/xv83/agcd-csiro/precip/daily/precip-total_AGCD-CSIRO_r005_19000101-20220405_daily_space-chunked.zarr
REF_SSR_FILE = precip-total-ssr_AGCD-CSIRO_r005_${REF_START}0101-${REF_END}1231_daily.nc

AF_FILE=${HIST_VAR}-${MAPPING}-adjustment-factors-${SCALING}-${GROUPING}-ssr_day_${OBS_DATASET}-${MODEL}_historical-${EXPERIMENT}_${RUN}_${HIST_START}0101-${HIST_END}1231.nc
QQ_BASE=${HIST_VAR}-${MAPPING}-${SCALING}-${GROUPING}-ssr_day_${OBS_DATASET}-${MODEL}_${EXPERIMENT}_${RUN}_${TARGET_START}0101-${TARGET_END}1231


PRO getSOL_JO_CONT, dir, FILE_EXIST, NDJO, RADIUS, MINT, OPAC, TEMP, TAU, FLUX1, FLUX2
;
;-----------------------DEFINE FILE-NAMES-------------------------------
;
fname=dir+'/outputIDL_JO.dat'
;
;-----------------------CHECK IF FILES EXIST----------------------------
;
FILE_EXIST=FILE_TEST(fname)
IF(FILE_EXIST EQ 0) THEN BEGIN
   PRINT, 'FILE DOES NOT EXIST: ', fname
   RETURN
ENDIF
;
;------------------------READ IN DATA FROM FILES------------------------
;
HEADER=''
;
RADIUS=FLTARR(NDJO)*1.D0
MINT=FLTARR(NDJO)*1.D0
OPAC=FLTARR(NDJO)*1.D0
TEMP=FLTARR(NDJO)*1.D0
TAU=FLTARR(NDJO)*1.D0
FLUX1=FLTARR(NDJO)*1.D0
FLUX2=FLTARR(NDJO)*1.D0
;
OPENR, 1, fname
   READF, 1, HEADER
   FOR I=0, NDJO-1 DO BEGIN
      READF, 1, VAR0, VAR1, VAR2, VAR3, VAR4, VAR5, VAR6, VAR7
      RADIUS(I)=VAR1
      MINT(I)=VAR2
      OPAC(I)=VAR3
      TEMP(I)=VAR4
      TAU(I)=VAR5
      FLUX1(I)=VAR6
      FLUX2(I)=VAR7
   ENDFOR
CLOSE, 1
;
RETURN
;
END

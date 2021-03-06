PRO GET_XYZ_INDX, XIN, YIN, ZIN, XARR, YARR, ZARR, NDXMAX, NDYMAX, NDZMAX, INDX_X1, INDX_X2, INDX_Y1, INDX_Y2, INDX_Z1, INDX_Z2, EXPOL
;
;-----------------------------------------------------------------------
;
;  FINDS INDICES OF GRID FOR A CUBE SURROUNDING THE POINT (XIN,YIN,ZIN)
;
;  INPUT:  COORDINATES OF POINT:             XIN, YIN, ZIN
;          DIMENSION OF GRID:                NDXMAX, NDYMAX, NDZMAX
;          X,Y,Z-GRID:                       XARR, YARR, ZARR
;  OUTPUT: INDICES OF X-GRID:                INDX_X1, INDX_X2
;          INDICES OF Y-GRID:                INDX_Y1, INDX_Y2
;          INDICES OF Z-GRID:                INDX_Z1, INDX_Z2
;          FLAG IF EXTRAPOLATION IS NEEDED:  EXPOL
;
;-----------------------------------------------------------------------
;
RMAX=MAX(XARR)
;
IF(XIN GE 0.D0) THEN BEGIN
   STARTX=NDXMAX-2
   ENDX=0
   ALPHA=-1
ENDIF ELSE BEGIN
   STARTX=1
   ENDX=NDXMAX-1
   ALPHA=1
ENDELSE
;
IF(YIN GE 0.D0) THEN BEGIN
   STARTY=NDYMAX-2
   ENDY=0
   BETA=-1
ENDIF ELSE BEGIN
   STARTY=1
   ENDY=NDYMAX-1
   BETA=1
ENDELSE
;
IF(ZIN GE 0.D0) THEN BEGIN
   STARTZ=NDZMAX-2
   ENDZ=0
   GAMMA=-1
ENDIF ELSE BEGIN
   STARTZ=1
   ENDZ=NDZMAX-1
   GAMMA=1
ENDELSE
;
INDX_X1=STARTX
INDX_X2=STARTX-ALPHA
FOR I=STARTX, ENDX, ALPHA DO BEGIN
   IF(ALPHA*XARR(I) GE ALPHA*XIN) THEN BEGIN
      INDX_X1=I
      INDX_X2=I-ALPHA
      BREAK
   ENDIF
ENDFOR
;
INDX_Y1=STARTY
INDX_Y2=STARTY-BETA
FOR I=STARTY, ENDY, BETA DO BEGIN
   IF(BETA*YARR(I) GE BETA*YIN) THEN BEGIN
      INDX_Y1=I
      INDX_Y2=I-BETA
      BREAK
   ENDIF
ENDFOR
;
INDX_Z1=STARTZ
INDX_Z2=STARTZ-GAMMA
FOR I=STARTZ, ENDZ, GAMMA DO BEGIN
   IF(GAMMA*ZARR(I) GE GAMMA*ZIN) THEN BEGIN
      INDX_Z1=I
      INDX_Z2=I-GAMMA
      BREAK
   ENDIF
ENDFOR
;
;--------------EXTRAPOLATION FOR GRID-POINTS NEAR PHOTOSPHERE-----------
;
;CHECK IF EXTRAPOLATION IS NEEDED AT INNER PART OF THE STAR
RAD=SQRT(XARR(INDX_X1)*XARR(INDX_X1)+YARR(INDX_Y1)*YARR(INDX_Y1)+ZARR(INDX_Z1)*ZARR(INDX_Z1))
;
IF(RAD LT 1.D0) THEN BEGIN
   EXPOL=1
   FOR I=1, 10 DO BEGIN
      INDX_X1=INDX_X1-ALPHA
      INDX_X2=INDX_X2-ALPHA
      INDX_Y1=INDX_Y1-BETA
      INDX_Y2=INDX_Y2-BETA
      INDX_Z1=INDX_Z1-GAMMA
      INDX_Z2=INDX_Z2-GAMMA
      RAD=SQRT(XARR(INDX_X1)*XARR(INDX_X1)+YARR(INDX_Y1)*YARR(INDX_Y1)+ZARR(INDX_Z1)*ZARR(INDX_Z1))
      IF(RAD GE 1.D0) THEN BEGIN
         BREAK
      ENDIF
   ENDFOR
   IF(RAD LT 1.D0) THEN BEGIN
      PRINT, 'ERROR IN GET_XYZ_INDX: RAD LT 1.D0 => EXTRAPOLATION OVER MORE THAN 10 GRID POINTS'
      STOP
   ENDIF
   RETURN
ENDIF ELSE BEGIN
   EXPOL=0
ENDELSE
;
;-------------EXTRAPOLATION FOR GRID POINTS LARGER THAN RMAX------------
;
;CHECK IF EXTRAPOLATION IS NEEDED AT OUTER PART OF THE STAR
RAD=SQRT(XARR(INDX_X2)*XARR(INDX_X2)+YARR(INDX_Y2)*YARR(INDX_Y2)+ZARR(INDX_Z2)*ZARR(INDX_Z2))
;

IF(RAD GT RMAX) THEN BEGIN
;BY DEFAULT: EXTRAPOLATION
   EXPOL1=1
   EXPOL2=1
   EXPOL3=1
   IF(ABS(XIN) LT 1.D-6  AND ABS(YIN) LT 1.D-6) THEN BEGIN
      PRINT, 'POINT IS ON Z-AXIS => NO EXTRAPOLATION NEEDED'
      EXPOL1=0
   ENDIF
   IF(ABS(XIN) LT 1.D-6 AND ABS(ZIN) LT 1.D-6) THEN BEGIN
      PRINT, 'POINT IS ON Y-AXIS => NO EXTRAPOLATION NEEDED'
      EXPOL2=0
   ENDIF
   IF(ABS(YIN) LT 1.D-6 AND ABS(ZIN) LT 1.D-6) THEN BEGIN
      PRINT, 'POINT IS ON X-AXIS => NO EXTRAPOLATION NEEDED'
      EXPOL3=0
   ENDIF
   IF(EXPOL1 EQ 0 OR EXPOL2 EQ 0 OR EXPOL3 EQ 0) THEN BEGIN
      EXPOL=0
   ENDIF ELSE BEGIN
      EXPOL=1
      FOR I=1, 10 DO BEGIN
         INDX_X1=INDX_X1+ALPHA
         INDX_X2=INDX_X2+ALPHA
         INDX_Y1=INDX_Y1+BETA
         INDX_Y2=INDX_Y2+BETA
         INDX_Z1=INDX_Z1+GAMMA
         INDX_Z2=INDX_Z2+GAMMA
         RAD=SQRT(XARR(INDX_X2)*XARR(INDX_X2)+YARR(INDX_Y2)*YARR(INDX_Y2)+ZARR(INDX_Z2)*ZARR(INDX_Z2))
         IF(RAD LE RMAX) THEN BEGIN
            BREAK
         ENDIF
      ENDFOR
      IF(RAD GT RMAX) THEN BEGIN
         PRINT, 'ERROR IN GET_XYZ_INDX: LINFO_MAX EQ FALSE => EXTRAPOLATION OVER MORE THAN 10 GRID POINTS'
      ENDIF
   ENDELSE
ENDIF ELSE BEGIN
   EXPOL=0
ENDELSE
;
;
;
END

subroutine mint_fvm3d
!
!-----------------------------------------------------------------------
!-----------calculates mean intensities at all grid point---------------
!-----------------------------------------------------------------------
!
!   formal solution from 3d finite volume method
!
!                  mu-integration between [-1,1]
!                 phi-integration between [0,2*pi]
!
!-----------------------------------------------------------------------
!
use prog_type
use fund_const
use dime3d, only: int3d, alocont_o_nn3d, alocont_nn3d, mint3d, normalization3d, fcontx3d, fconty3d, fcontz3d, &
                  alocont_nn3d_tmp, mint3d_tmp, normalization3d_tmp, fcontx3d_tmp, fconty3d_tmp, fcontz3d_tmp, &
                  kcontxx3d_tmp, kcontyy3d_tmp, kcontzz3d_tmp, kcontxy3d_tmp, kcontxz3d_tmp, kcontyz3d_tmp, &
                  kcontxx3d, kcontyy3d, kcontzz3d, kcontxy3d, kcontxz3d, kcontyz3d, &                  
                  ndxmax, ndymax, ndzmax, imask3d
use angles, only: dim_omega
use timing, only: ttot_it_fvm
!
implicit none
!
! ... local scalars
integer(i4b) :: i, j, k
integer(i4b) :: xobsindx
integer(i4b) :: oindx
integer(i4b) :: err
integer(i4b) :: ndxyz
real(dp) :: ts, te
integer(i4b) :: nticks_sec, nticks_max, nticks_initial, nticks_final
!
! ... local arrays
!
! ... local functions
!
! ... local characters
!
alocont_nn3d=zero
normalization3d=zero
mint3d=zero
fcontx3d=zero
fconty3d=zero
fcontz3d=zero
kcontxx3d=zero
kcontyy3d=zero
kcontzz3d=zero
kcontxy3d=zero
kcontxz3d=zero
kcontyz3d=zero
!
!--------------deallocation of global (threadprivate) arrays------------
!
if(allocated(int3d)) deallocate(int3d)
if(allocated(alocont_o_nn3d)) deallocate(alocont_o_nn3d)
!
!-----------------------begin of parallel region------------------------
!
call system_clock(count=nticks_initial, count_rate=nticks_sec, count_max=nticks_max)
!
!$omp parallel &
!$omp private(err, oindx)
!
!-------------allocation of global (threadprivate) arrays---------------
!
   allocate(alocont_o_nn3d(ndxmax,ndymax,ndzmax,27), stat=err)
      if(err.ne.0) stop 'allocation error in mint_fvm3d: alocont_o_nn3d'
   allocate(alocont_nn3d_tmp(ndxmax,ndymax,ndzmax,27), stat=err)
      if(err.ne.0) stop 'allocation error in mint_fvm3d: alocont_nn3d_tmp'
   allocate(normalization3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: normalization3d_tmp'
   allocate(mint3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: mint3d_tmp'
   allocate(fcontx3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: fcontx3d_tmp'
   allocate(fconty3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: fconty3d_tmp'
   allocate(fcontz3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: fcontz3d_tmp'
   allocate(int3d(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_fvm3d: int3d'
   allocate(kcontxx3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontxx3d_tmp'
   allocate(kcontyy3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontyy3d_tmp'
   allocate(kcontzz3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontzz3d_tmp'
   allocate(kcontxy3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontxy3d_tmp'
   allocate(kcontxz3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontxz3d_tmp'
   allocate(kcontyz3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mint_sc3d: kcontyz3d_tmp'      


!
   alocont_nn3d_tmp=zero
   normalization3d_tmp=zero
   mint3d_tmp=zero
   fcontx3d_tmp=zero
   fconty3d_tmp=zero
   fcontz3d_tmp=zero
   kcontxx3d_tmp=zero
   kcontyy3d_tmp=zero
   kcontzz3d_tmp=zero
   kcontxy3d_tmp=zero
   kcontxz3d_tmp=zero
   kcontyz3d_tmp=zero
!
!-----------------------------------------------------------------------
!
   !$omp do schedule(dynamic)
      do oindx=1, dim_omega
!         write(*,*) 'calculating omega', oindx, dim_omega
         call ffvm_cont3d(oindx)
      enddo
   !$omp enddo
!
!------------------------add up temporary arrays------------------------
!
   !$omp critical
      alocont_nn3d = alocont_nn3d+alocont_nn3d_tmp
      normalization3d = normalization3d + normalization3d_tmp
      mint3d = mint3d + mint3d_tmp
      fcontx3d = fcontx3d + fcontx3d_tmp
      fconty3d = fconty3d + fconty3d_tmp
      fcontz3d = fcontz3d + fcontz3d_tmp
      kcontxx3d = kcontxx3d + kcontxx3d_tmp
      kcontyy3d = kcontyy3d + kcontyy3d_tmp
      kcontzz3d = kcontzz3d + kcontzz3d_tmp
      kcontxy3d = kcontxy3d + kcontxy3d_tmp
      kcontxz3d = kcontxz3d + kcontxz3d_tmp
      kcontyz3d = kcontyz3d + kcontyz3d_tmp      
   !$omp end critical
!
!------------deallocation of global (threadprivate) arrays--------------
!
   deallocate(alocont_nn3d_tmp)
   deallocate(normalization3d_tmp)
   deallocate(mint3d_tmp)
   deallocate(fcontx3d_tmp)
   deallocate(fconty3d_tmp)
   deallocate(fcontz3d_tmp)
   deallocate(kcontxx3d_tmp)
   deallocate(kcontyy3d_tmp)
   deallocate(kcontzz3d_tmp)
   deallocate(kcontxy3d_tmp)
   deallocate(kcontxz3d_tmp)
   deallocate(kcontyz3d_tmp)   
   deallocate(alocont_o_nn3d)
   deallocate(int3d)
!
!$omp end parallel
!  
!renormalize
do i=3, ndxmax-2
   do j=3, ndymax-2
      do k=3, ndzmax-2
         select case(imask3d(i,j,k))
            case(1,2,3)
               if(abs(normalization3d(i,j,k)-0.d0).lt.1.d-6) then
                  write(*,'(a50, 3i5, es20.8)') 'normalization error in mint_fvm3d:', i, j, k, normalization3d(i,j,k)
                  normalization3d(i,j,k)=1.d0
                  stop
               endif
               mint3d(i,j,k) = mint3d(i,j,k)/normalization3d(i,j,k)
               alocont_nn3d(i,j,k,:) = alocont_nn3d(i,j,k,:)/normalization3d(i,j,k)
               normalization3d(i,j,k) = normalization3d(i,j,k)/normalization3d(i,j,k)
               fcontx3d(i,j,k) = fcontx3d(i,j,k)/normalization3d(i,j,k)
               fconty3d(i,j,k) = fconty3d(i,j,k)/normalization3d(i,j,k)
               fcontz3d(i,j,k) = fcontz3d(i,j,k)/normalization3d(i,j,k)
               kcontxx3d(i,j,k) = kcontxx3d(i,j,k)/normalization3d(i,j,k)
               kcontyy3d(i,j,k) = kcontyy3d(i,j,k)/normalization3d(i,j,k)
               kcontzz3d(i,j,k) = kcontzz3d(i,j,k)/normalization3d(i,j,k)
               kcontxy3d(i,j,k) = kcontxy3d(i,j,k)/normalization3d(i,j,k)
               kcontxz3d(i,j,k) = kcontxz3d(i,j,k)/normalization3d(i,j,k)
               kcontyz3d(i,j,k) = kcontyz3d(i,j,k)/normalization3d(i,j,k)
            case default
         end select
      enddo
   enddo
enddo
!
call system_clock(count=nticks_final)
write(*,*)
write(*,*) 'time for all angles (fvm)', dble(nticks_final-nticks_initial)/nticks_sec
write(*,*)
ttot_it_fvm=ttot_it_fvm+dble(nticks_final-nticks_initial)/nticks_sec
!
!
!
end subroutine mint_fvm3d
!
!-----------------------------------------------------------------------
!-----------------------------------------------------------------------
!-----------------------------------------------------------------------
!
subroutine mintbar_fvm3d
!
!-----------------------------------------------------------------------
!--calculates frequency integrated mean intensities at all grid points--
!-----------------------------------------------------------------------
!
!   formal solution from 3d finite volume method
!       
!                  mu-integration between [-1,1]
!                 phi-integration between [0,2*pi]
!                xobs-integration between [-vmax-3, vmax+3]
!
!-----------------------------------------------------------------------
!
use prog_type
use fund_const
use dime3d, only: ndxmax, ndymax, ndzmax, int3d, aloline_on_nn3d, aloline_nn3d, aloline_nn3d_tmp, &
                  mintbar3d, mintbar3d_tmp, normalization3d, normalization3d_tmp, &
                  imask3d
use angles, only: dim_omega
use freq, only: nxobs
use omp_lib
!
implicit none
!
! ... local scalars
integer(i4b) :: i, j, k
integer(i4b) :: oindx, xobsindx
integer(i4b) :: err
integer(i4b) :: nticks_sec, nticks_max, nticks_initial, nticks_final
!
! ... local arrays
!
! ... local functions
!
! ... local characters
!
!------------calculating intensities for given nodes--------------------
!
aloline_nn3d=0.d0
normalization3d=0.d0
mintbar3d=0.d0
!
!--------------deallocation of global (threadprivate) arrays------------
!
if(allocated(int3d)) deallocate(int3d)
if(allocated(aloline_on_nn3d)) deallocate(aloline_on_nn3d)
!
!-----------------------begin of parallel region------------------------
!
call system_clock(count=nticks_initial, count_rate=nticks_sec, count_max=nticks_max)
!
!$omp parallel &
!$omp private(err, oindx, xobsindx)
!
!-------------allocation of global (threadprivate) arrays---------------
!
   allocate(aloline_on_nn3d(ndxmax,ndymax,ndzmax,27), stat=err)
      if(err.ne.0) stop 'allocation error in mintbar_fvm3d: aloline_on_nn3d'
!
   allocate(aloline_nn3d_tmp(ndxmax,ndymax,ndzmax,27), stat=err)
      if(err.ne.0) stop 'allocation error in mintbar_fvm3d: aloline_nn3d_tmp'
!
   allocate(normalization3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mintbar_fvm3d: normalization3d_tmp'
!
   allocate(mintbar3d_tmp(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mintbar_fvm3d: mintbar3d_tmp'
!
   allocate(int3d(ndxmax,ndymax,ndzmax), stat=err)
      if(err.ne.0) stop 'allocation error mintbar_fvm3d: int3d'
!
   aloline_nn3d_tmp=0.d0
   normalization3d_tmp=0.d0
   mintbar3d_tmp=0.d0
!
!-----------------------------------------------------------------------
!
!   !$omp do schedule(static)
   !$omp do schedule(dynamic)
   do xobsindx=1, nxobs
      write(*,'(a55,i4, a1, i4)') 'calculating all angles for (freq-point/nxobs)', xobsindx, '/', nxobs
      do oindx=1, dim_omega
         call ffvm_line3d(oindx,xobsindx)
      enddo
   enddo
   !$omp enddo
!
!------------------------add up temporary arrays------------------------
!
   !$omp critical
      aloline_nn3d = aloline_nn3d+aloline_nn3d_tmp
      normalization3d = normalization3d + normalization3d_tmp
      mintbar3d = mintbar3d + mintbar3d_tmp
   !$omp end critical
!
!------------deallocation of global (threadprivate) arrays--------------
!
   deallocate(aloline_nn3d_tmp)
   deallocate(normalization3d_tmp)
   deallocate(mintbar3d_tmp)
   deallocate(aloline_on_nn3d)
   deallocate(int3d)
!
!$omp end parallel
!
!renormalize
do i=3, ndxmax-2
   do j=3, ndymax-2
      do k=3, ndzmax-2
         select case(imask3d(i,j,k))
            case(1,2,3)
               if(abs(normalization3d(i,j,k)-0.d0).lt.1.d-6) then
                  write(*,'(a50, 3i5, es20.8)') 'normalization error in mintbar_fvm3d:', i, j, k, normalization3d(i,j,k)
                  write(*,*) i, j, k, normalization3d(i,j,k)
                  normalization3d(i,j,k)=1.d0
                  stop
               endif
               mintbar3d(i,j,k) = mintbar3d(i,j,k)/normalization3d(i,j,k)
               aloline_nn3d(i,j,k,:) = aloline_nn3d(i,j,k,:)/normalization3d(i,j,k)
               normalization3d(i,j,k) = normalization3d(i,j,k)/normalization3d(i,j,k)
            case default
         end select
      enddo
   enddo
enddo
!
call system_clock(count=nticks_final)
write(*,*)
write(*,*) 'time for all angles and frequencies', dble(nticks_final-nticks_initial)/nticks_sec
!
!
end subroutine mintbar_fvm3d

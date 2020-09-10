 start {molname} 
 title "{description}"
 charge {charge} 

 geometry units au  
 {structure}
 end  
 basis  
   * library {basis}  
 end
 dft
 xc {functional}
 mult {mult}
 end
task {method} energy

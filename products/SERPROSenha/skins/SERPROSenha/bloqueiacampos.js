function Inibe(boqueio){
   if (boqueio == 1){
       document.edit_form.qtd_tentativas.disabled = false;
       document.edit_form.mnt_lock.disabled = false;
   }
   if (boqueio== 2 ){
       document.edit_form.qtd_tentativas.disabled = true;
       document.edit_form.mnt_lock.disabled = true;
   }
}

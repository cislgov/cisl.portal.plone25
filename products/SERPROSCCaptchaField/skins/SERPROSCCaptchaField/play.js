function play() 
{ 
  document.getElementById("playAudio").innerHTML = '';
  document.getElementById("playAudio").innerHTML='<EMBED SRC= captchaSonoro.mp3?'+new Date().getTime()+' HIDDEN="true" AUTOSTART="true" MASTERSOUND/>';

  document.getElementById("__ac_captcha").value="";
  document.getElementById("__ac_captcha").focus();

} 

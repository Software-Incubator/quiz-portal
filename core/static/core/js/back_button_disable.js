// function preventBack(){window.history.forward();}
//     setTimeout("preventBack()", 0);
//     window.onunload=function(){null};

window.location.hash="no-back-button";
window.location.hash="Again-No-back-button";
window.onhashchange=function(){window.location.hash="#";}
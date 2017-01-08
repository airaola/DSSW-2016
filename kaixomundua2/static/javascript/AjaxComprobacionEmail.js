function AjaxComprobacionEmail () {
	
  var XMLHttpRequestObject = new XMLHttpRequest();
  var correoDeAjax = document.getElementById("email");
  var correoParaValidacion = "?emailAjax=" + correoDeAjax.value;
  var respuesta;

  if(XMLHttpRequestObject)
  {
    XMLHttpRequestObject.onreadystatechange = function()
    {
      if (XMLHttpRequestObject.readyState==4)
      {
        respuesta = XMLHttpRequestObject.responseText;
        if (respuesta == ""){
          document.getElementById("emailBien").innerHTML = ("Email correcto! ");
          document.getElementById("emailMal").innerHTML= "";
        }
        else{
          document.getElementById("emailBien").innerHTML = "";
          document.getElementById("emailMal").innerHTML= respuesta;
        }
      }
    }
  }
	XMLHttpRequestObject.open ( "get", "/validacion" + correoParaValidacion, true );
    XMLHttpRequestObject.send(null);
  
}